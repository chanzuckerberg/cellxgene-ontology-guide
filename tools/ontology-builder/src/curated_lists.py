# #### Hand-Curation of Systems and Organs
# Systems and organs were hand-curated in this [spreadsheet](
# https://docs.google.com/spreadsheets/d/18761SLamZUN9FLAMV_zmg0lutSSUkArCEs8GnprxtZE/edit#gid=717648045).
#

# #### Tissue Constants

# Hand-curated systems.
SYSTEM_TISSUES = [
    "UBERON_0001017",
    "UBERON_0004535",
    "UBERON_0001009",
    "UBERON_0001007",
    "UBERON_0000922",
    "UBERON_0000949",
    "UBERON_0002330",
    "UBERON_0002390",
    "UBERON_0002405",
    "UBERON_0000383",
    "UBERON_0001016",
    "UBERON_0000010",
    "UBERON_0001008",
    "UBERON_0000990",
    "UBERON_0001004",
    "UBERON_0001032",
    "UBERON_0001434",
]

# Hand-curated organs.
ORGAN_TISSUES = [
    "UBERON_0000992",
    "UBERON_0000029",
    "UBERON_0002048",
    "UBERON_0002110",
    "UBERON_0001043",
    "UBERON_0003889",
    "UBERON_0018707",
    "UBERON_0000178",
    "UBERON_0002371",
    "UBERON_0000955",
    "UBERON_0000310",
    "UBERON_0000970",
    "UBERON_0000948",
    "UBERON_0000160",
    "UBERON_0002113",
    "UBERON_0002107",
    "UBERON_0000004",
    "UBERON_0001264",
    "UBERON_0001987",
    "UBERON_0002097",
    "UBERON_0002240",
    "UBERON_0002106",
    "UBERON_0000945",
    "UBERON_0002370",
    "UBERON_0002046",
    "UBERON_0001723",
    "UBERON_0000995",
    "UBERON_0001013",
]

# Production tissues with no corresponding hand-curated system; required so
# that they are explicitly added to the generated subgraph.
# TODO generate using https://app.zenhub.com/workspaces/single-cell-5e2a191dad828d52cc78b028/issues/gh/chanzuckerberg
#  /single-cell-data-portal/6227
ORPHAN_TISSUES = [
    "UBERON_0001013",  # adipose tissue
    "UBERON_0009472",  # axilla
    "UBERON_0018707",  # bladder organ
    "UBERON_0000310",  # breast
    "UBERON_0001348",  # brown adipose
    "UBERON_0007106",  # chorionic villus
    "UBERON_0000030",  # lamina propria
    "UBERON_0015143",  # mesenteric fat pad
    "UBERON_0000344",  # mucosa
    "UBERON_0003688",  # omentum
    "UBERON_0001264",  # pancreas
    "UBERON_0000175",  # pleural effusion
    "UBERON_0000403",  # scalp
    "UBERON_0001836",  # saliva
    "UBERON_0001416",  # skin of abdomen
    "UBERON_0002097",  # skin of body
    "UBERON_0001868",  # skin of chest
    "UBERON_0001511",  # skin of leg
    "UBERON_0002190",  # subcutaneous adipose tissue
    "UBERON_0002100",  # trunk
    "UBERON_0035328",  # upper outer quadrant of breast
    "UBERON_0001040",  # yolk sac
    "UBERON_0000014",  # zone of skin
]

TISSUE_GENERAL = [
    "UBERON_0000178",  # blood
    "UBERON_0002048",  # lung
    "UBERON_0002106",  # spleen
    "UBERON_0002371",  # bone marrow
    "UBERON_0002107",  # liver
    "UBERON_0002113",  # kidney
    "UBERON_0000955",  # brain
    "UBERON_0002240",  # spinal cord
    "UBERON_0000310",  # breast
    "UBERON_0000948",  # heart
    "UBERON_0002097",  # skin of body
    "UBERON_0000970",  # eye
    "UBERON_0001264",  # pancreas
    "UBERON_0001043",  # esophagus
    "UBERON_0001155",  # colon
    "UBERON_0000059",  # large intestine
    "UBERON_0002108",  # small intestine
    "UBERON_0000160",  # intestine
    "UBERON_0000945",  # stomach
    "UBERON_0001836",  # saliva
    "UBERON_0001723",  # tongue
    "UBERON_0001013",  # adipose tissue
    "UBERON_0000473",  # testis
    "UBERON_0002367",  # prostate gland
    "UBERON_0000057",  # urethra
    "UBERON_0000056",  # ureter
    "UBERON_0003889",  # fallopian tube
    "UBERON_0000995",  # uterus
    "UBERON_0000992",  # ovary
    "UBERON_0002110",  # gall bladder
    "UBERON_0001255",  # urinary bladder
    "UBERON_0018707",  # bladder organ
    "UBERON_0000922",  # embryo
    "UBERON_0004023",  # ganglionic eminence --> this a part of the embryo, remove in case generality is desired
    "UBERON_0001987",  # placenta
    "UBERON_0007106",  # chorionic villus
    "UBERON_0002369",  # adrenal gland
    "UBERON_0002368",  # endocrine gland
    "UBERON_0002365",  # exocrine gland
    "UBERON_0000030",  # lamina propria
    "UBERON_0000029",  # lymph node
    "UBERON_0004536",  # lymph vasculature
    "UBERON_0001015",  # musculature
    "UBERON_0000004",  # nose
    "UBERON_0003688",  # omentum
    "UBERON_0000977",  # pleura
    "UBERON_0002370",  # thymus
    "UBERON_0002049",  # vasculature
    "UBERON_0009472",  # axilla
    "UBERON_0001087",  # pleural fluid
    "UBERON_0000344",  # mucosa
    "UBERON_0001434",  # skeletal system
    "UBERON_0002228",  # rib
    "UBERON_0003129",  # skull
    "UBERON_0004537",  # blood vasculature
    "UBERON_0002405",  # immune system
    "UBERON_0001009",  # circulatory system
    "UBERON_0001007",  # digestive system
    "UBERON_0001017",  # central nervous system
    "UBERON_0001008",  # renal system
    "UBERON_0000990",  # reproductive system
    "UBERON_0001004",  # respiratory system
    "UBERON_0000010",  # peripheral nervous system
    "UBERON_0001032",  # sensory system
    "UBERON_0002046",  # thyroid gland
    "UBERON_0004535",  # cardiovascular system
    "UBERON_0000949",  # endocrine system
    "UBERON_0002330",  # exocrine system
    "UBERON_0002390",  # hematopoietic system
    "UBERON_0000383",  # musculature of body
    "UBERON_0001465",  # knee
    "UBERON_0001016",  # nervous system
    "UBERON_0001348",  # brown adipose tissue
    "UBERON_0015143",  # mesenteric fat pad
    "UBERON_0000175",  # pleural effusion
    "UBERON_0001416",  # skin of abdomen
    "UBERON_0001868",  # skin of chest
    "UBERON_0001511",  # skin of leg
    "UBERON_0002190",  # subcutaneous adipose tissue
    "UBERON_0000014",  # zone of skin
    "UBERON_0000916",  # abdomen
]

# ### Cell Type Constants
# Hand-Curation of Cell Classes and Cell Subclasses
# Cell classes and cell subclasses were hand-curated in this [spreadsheet](
# https://docs.google.com/spreadsheets/d/1ebGc-LgZJhNsKinzQZ3rpzuh1e1reSH3Rcbn88mCOaU/edit#gid=1625183014).

# Hand-curated cell classes.
CELL_CLASSES = [
    "CL_0002494",  # cardiocyte
    "CL_0002320",  # connective tissue cell
    "CL_0000473",  # defensive cell
    "CL_0000066",  # epithelial cell
    "CL_0000988",  # hematopoietic cell
    "CL_0002319",  # neural cell
    "CL_0011115",  # precursor cell
    "CL_0000151",  # secretory cell
    "CL_0000039",  # germ cell line
    "CL_0000064",  # ciliated cell
    "CL_0000183",  # contractile cell
    "CL_0000188",  # cell of skeletal muscle
    "CL_0000219",  # motile cell
    "CL_0000325",  # stuff accumulating cell
    "CL_0000349",  # extraembryonic cell
    "CL_0000586",  # germ cell
    "CL_0000630",  # supporting cell
    "CL_0001035",  # bone cell
    "CL_0001061",  # abnormal cell
    "CL_0002321",  # embryonic cell (metazoa)
    "CL_0009010",  # transit amplifying cell
    "CL_1000600",  # lower urinary tract cell
    "CL_4033054",  # perivascular cell
]

# Hand-curated cell subclasses.
CELL_SUBCLASSES = [
    "CL_0000624",  # CD4-positive, alpha-beta T cell
    "CL_0000625",  # CD8-positive, alpha-beta T cell
    "CL_0000084",  # T cell
    "CL_0000236",  # B cell
    "CL_0000451",  # dendritic cell
    "CL_0000576",  # monocyte
    "CL_0000235",  # macrophage
    "CL_0000542",  # lymphocyte
    "CL_0000738",  # leukocyte
    "CL_0000763",  # myeloid cell
    "CL_0008001",  # hematopoietic precursor cell
    "CL_0000234",  # phagocyte
    "CL_0000679",  # glutamatergic neuron
    "CL_0000617",  # GABAergic neuron
    "CL_0000099",  # interneuron
    "CL_0000125",  # glial cell
    "CL_0000101",  # sensory neuron
    "CL_0000100",  # motor neuron
    "CL_0000117",  # CNS neuron (sensu Vertebrata)
    "CL_0000540",  # neuron
    "CL_0000669",  # pericyte
    "CL_0000499",  # stromal cell
    "CL_0000057",  # fibroblast
    "CL_0000152",  # exocrine cell
    "CL_0000163",  # endocrine cell
    "CL_0000115",  # endothelial cell
    "CL_0002076",  # endo-epithelial cell
    "CL_0002078",  # meso-epithelial cell
    "CL_0011026",  # progenitor cell
    "CL_0000015",  # male germ cell
    "CL_0000021",  # female germ cell
    "CL_0000034",  # stem cell
    "CL_0000055",  # non-terminally differentiated cell
    "CL_0000068",  # duct epithelial cell
    "CL_0000075",  # columnar/cuboidal epithelial cell
    "CL_0000076",  # squamous epithelial cell
    "CL_0000079",  # stratified epithelial cell
    "CL_0000082",  # epithelial cell of lung
    "CL_0000083",  # epithelial cell of pancreas
    "CL_0000095",  # neuron associated cell
    "CL_0000098",  # sensory epithelial cell
    "CL_0000136",  # fat cell
    "CL_0000147",  # pigment cell
    "CL_0000150",  # glandular epithelial cell
    "CL_0000159",  # seromucus secreting cell
    "CL_0000182",  # hepatocyte
    "CL_0000186",  # myofibroblast cell
    "CL_0000187",  # muscle cell
    "CL_0000221",  # ectodermal cell
    "CL_0000222",  # mesodermal cell
    "CL_0000244",  # urothelial cell
    "CL_0000351",  # trophoblast cell
    "CL_0000584",  # enterocyte
    "CL_0000586",  # germ cell
    "CL_0000670",  # primordial germ cell
    "CL_0000680",  # muscle precursor cell
    "CL_0001063",  # neoplastic cell
    "CL_0002077",  # ecto-epithelial cell
    "CL_0002222",  # vertebrate lens cell
    "CL_0002327",  # mammary gland epithelial cell
    "CL_0002503",  # adventitial cell
    "CL_0002518",  # kidney epithelial cell
    "CL_0002535",  # epithelial cell of cervix
    "CL_0002536",  # epithelial cell of amnion
    "CL_0005006",  # ionocyte
    "CL_0008019",  # mesenchymal cell
    "CL_0008034",  # mural cell
    "CL_0009010",  # transit amplifying cell
    "CL_1000296",  # epithelial cell of urethra
    "CL_1000497",  # kidney cell
    "CL_2000004",  # pituitary gland cell
    "CL_2000064",  # ovarian surface epithelial cell
    "CL_4030031",  # interstitial cell
    "CL_0002494",  # cardiocyte
]

# Production cell types with no corresponding hand-curated cell class; required
# so that they are explicitly added to the generated subgraph.
# TODO check if this can be generated as part of
#  https://app.zenhub.com/workspaces/single-cell-5e2a191dad828d52cc78b028/issues/gh/chanzuckerberg/single-cell-data
#  -portal/6227
ORPHAN_CELL_TYPES = [
    "CL_0000003",
    "CL_0009012",
    "CL_0000064",
    "CL_0000548",
    "CL_0000677",
    "CL_0000186",
    "CL_0009011",
    "CL_1001319",
    "CL_0000188",
    "CL_1000497",
    "CL_0008019",
    "CL_1000597",
    "CL_1000500",
    "CL_1000271",
    "CL_0000663",
    "CL_0000255",
    "CL_0001034",
    "CL_0001063",
    "CL_0011101",
    "CL_0008036",
    "CL_0000525",
    "CL_0002488",
    "CL_0000148",
    "CL_0001064",
    "CL_0002092",
    "CL_0002371",
    "CL_0009005",
    "CL_0000019",
    "CL_0000114",
    "CL_0000630",
    "CL_0008034",
    "CL_0000010",
    "CL_0009002",
    "CL_0000670",
    "CL_0000222",
    "CL_0009010",
    "CL_0000001",
    "CL_0000183",
    "CL_1000458",
    "CL_2000021",
    "CL_0001061",
]
