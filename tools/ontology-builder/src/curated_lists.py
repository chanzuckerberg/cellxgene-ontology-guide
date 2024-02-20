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
