"""
Extract "meaning modifier" markers (intensifier, downtoner, negation, hedge,
reinforcer, concession) relative to a target lemma, across a
previous / lemma / following sentence triplet.

Design notes (see chat for the full explanation):
- Sentences are parsed SEPARATELY, not concatenated + re-split, so your
  existing sentence boundaries are trusted rather than re-derived by spaCy.
- A running token offset gives every token a position in one shared
  integer space, so distances are comparable across sentence boundaries.
- Category is carried by the Matcher's match_id, so word -> category
  lookup never needs a manual dict scan.
- One MarkerHit row per marker occurrence (one-to-many vs. your source id).
"""

import spacy
from spacy.matcher import Matcher
from dataclasses import dataclass
from typing import Optional, List

nlp = spacy.load("en_core_web_sm")

MARKERS = {
    "intensifier": {
        "very", "really", "extremely", "highly", "deeply", "utterly",
        "completely", "totally", "absolutely",
    },
    "downtoner": {
        "rather", "fairly", "quite", "somewhat", "slightly", "barely",
        "hardly", "almost",
    },
    "negation": {
        "not", "never", "neither", "nor", "no",
    },
    "hedge": {
        "perhaps", "probably", "possibly", "apparently", "seemingly", "maybe",
    },
    "reinforcer": {
        "certainly", "clearly", "indeed", "undoubtedly", "surely", "definitely",
    },
    "concession": {
        "but", "however", "although", "though", "yet", "nevertheless",
        "nonetheless", "still",
    },
}


def build_matcher(nlp) -> Matcher:
    """One Matcher pattern per marker word, keyed by category via match_id.
    Also doubles as a duplicate-assignment check across categories."""
    seen = {}
    matcher = Matcher(nlp.vocab)
    for category, words in MARKERS.items():
        for w in words:
            if w in seen and seen[w] != category:
                raise ValueError(
                    f"'{w}' assigned to both '{seen[w]}' and '{category}'"
                )
            seen[w] = category
        patterns = [[{"LOWER": w}] for w in words]
        matcher.add(category, patterns)
    return matcher


MATCHER = build_matcher(nlp)


@dataclass
class MarkerHit:
    source_id: str                      # FK back to your existing lemma-sentence id
    sentence_position: str              # 'previous' | 'lemma' | 'following'
    marker_text: str                    # surface form, e.g. "Nevertheless"
    marker_lemma: str                   # spaCy lemma of the marker token
    marker_category: str                # e.g. 'concession'
    lemma_present_in_sentence: bool     # target lemma occurs in THIS sentence
    marker_token_idx: int               # position in the shared 3-sentence space
    lemma_token_idx: Optional[int]      # anchor token's position, if any
    distance: Optional[int]             # signed: marker_idx - lemma_idx


def process_triplet(
    source_id: str,
    prev_text: Optional[str],
    lemma_text: Optional[str],
    foll_text: Optional[str],
    target_lemma: str,
) -> List[MarkerHit]:
    """
    prev_text / lemma_text / foll_text: raw sentence strings, already
    segmented by your existing pipeline (can be None/"" if missing, e.g.
    lemma sentence is the first sentence of the work -> no 'previous').
    target_lemma: the lemma you're tracking, e.g. 'foot'.
    """
    parts = [("previous", prev_text), ("lemma", lemma_text), ("following", foll_text)]

    docs, offsets = {}, {}
    running_offset = 0
    for name, text in parts:
        if text:
            d = nlp(text)
            docs[name] = d
            offsets[name] = running_offset
            running_offset += len(d)

    # Anchor: first occurrence of target_lemma in the lemma sentence.
    # (If it occurs more than once, this picks the first -- document that
    # choice if it matters for your analysis, and lemma_token_idx below
    # lets you always trace back which occurrence was used.)
    lemma_global_idx = None
    if "lemma" in docs:
        for tok in docs["lemma"]:
            if tok.lemma_.lower() == target_lemma.lower():
                lemma_global_idx = offsets["lemma"] + tok.i
                break

    hits: List[MarkerHit] = []
    for name, doc in docs.items():
        lemma_present_here = any(
            t.lemma_.lower() == target_lemma.lower() for t in doc
        )
        for match_id, start, _end in MATCHER(doc):
            token = doc[start]
            category = nlp.vocab.strings[match_id]
            global_idx = offsets[name] + token.i
            distance = (
                global_idx - lemma_global_idx
                if lemma_global_idx is not None
                else None
            )
            hits.append(MarkerHit(
                source_id=source_id,
                sentence_position=name,
                marker_text=token.text,
                marker_lemma=token.lemma_,
                marker_category=category,
                lemma_present_in_sentence=lemma_present_here,
                marker_token_idx=global_idx,
                lemma_token_idx=lemma_global_idx,
                distance=distance,
            ))
    return hits


if __name__ == "__main__":
    example = process_triplet(
        source_id="melville-moby-dick_s0042_l01",
        prev_text="He walked slowly toward the shore.",
        lemma_text="His foot was certainly not steady on the wet rocks.",
        foll_text="Nevertheless, he pressed on.",
        target_lemma="foot",
    )
    for hit in example:
        print(hit)
