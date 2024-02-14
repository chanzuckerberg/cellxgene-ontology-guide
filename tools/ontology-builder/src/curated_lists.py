# #### Hand-Curation of Systems and Organs
# Systems and organs were hand-curated in this [spreadsheet](https://docs.google.com/spreadsheets/d/18761SLamZUN9FLAMV_zmg0lutSSUkArCEs8GnprxtZE/edit#gid=717648045).
#

# #### Tissue Constants

# Hand-curated systems.
system_tissues = [
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
organ_tissues = [
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
# TODO generate using https://app.zenhub.com/workspaces/single-cell-5e2a191dad828d52cc78b028/issues/gh/chanzuckerberg/single-cell-data-portal/6227
orphan_tissues = [
    "UBERON_0001013",  # adipose tissue
    "UBERON_0009472",  # 	axilla
    "UBERON_0018707",  # bladder organ
    "UBERON_0000310",  # breast
    "UBERON_0001348",  # brown adipose
    "UBERON_0007106",  # 	chorionic villus
    "UBERON_0000030",  # 	lamina propria
    "UBERON_0015143",  # mesenteric fat pad
    "UBERON_0000344",  # mucosa
    "UBERON_0003688",  # 	omentum
    "UBERON_0001264",  # pancreas
    "UBERON_0000175",  # 	pleural effusion
    "UBERON_0000403",  # scalp
    "UBERON_0001836",  # 	saliva
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


# ### Cell Type Constants
# Hand-Curation of Cell Classes and Cell Subclasses
# Cell classes and cell subclasses were hand-curated in this [spreadsheet](https://docs.google.com/spreadsheets/d/1ebGc-LgZJhNsKinzQZ3rpzuh1e1reSH3Rcbn88mCOaU/edit#gid=1625183014).

# Hand-curated cell classes.
cell_classes = [
    "CL_0002494",
    "CL_0002320",
    "CL_0000473",
    "CL_0000066",
    "CL_0000988",
    "CL_0000187",
    "CL_0002319",
    "CL_0011115",
    "CL_0000151",
]

# Hand-curated cell subclasses.
cell_subclasses = [
    "CL_0000738",
    "CL_0000542",
    "CL_0000763",
    "CL_0000084",
    "CL_0002076",
    "CL_0002078",
    "CL_0000540",
    "CL_0011026",
    "CL_0000115",
    "CL_0008001",
    "CL_0000163",
    "CL_0000236",
    "CL_0000099",
    "CL_0000234",
    "CL_0000624",
    "CL_0000057",
    "CL_0000125",
    "CL_0000117",
    "CL_0000235",
    "CL_0000451",
    "CL_0000625",
    "CL_0000679",
    "CL_0000617",
    "CL_0000499",
    "CL_0000576",
    "CL_0000101",
    "CL_0000669",
    "CL_0000152",
    "CL_0000100",
]

# Production cell types with no corresponding hand-curated cell class; required
# so that they are explicitly added to the generated subgraph.
# TODO check if this can be generated as part of https://app.zenhub.com/workspaces/single-cell-5e2a191dad828d52cc78b028/issues/gh/chanzuckerberg/single-cell-data-portal/6227
orphan_cell_types = [
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
