"""Citation text shared by the CLI and GUI (`isotherm-fit cite` / Cite dialog)."""

from isotherm_fit import __version__

CITATION_APA = (
    "Khachatryan, K. (2026). isotherm-fit: automated fitting of moisture sorption "
    "isotherm models for food stability assessment (Version "
    f"{__version__}) [Computer software]. "
    "University of Agriculture in Krakow. https://doi.org/10.5281/zenodo.PENDING"
)

CITATION_BIBTEX = f"""@software{{khachatryan_isotherm_fit_2026,
  author  = {{Khachatryan, Karen}},
  title   = {{isotherm-fit: automated fitting of moisture sorption isotherm models for food stability assessment}},
  year    = {{2026}},
  version = {{{__version__}}},
  doi     = {{10.5281/zenodo.PENDING}},
  url     = {{https://github.com/karenkhachatryan-lab/isotherm-fit}}
}}"""
