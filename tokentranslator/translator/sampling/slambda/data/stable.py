# name for extracting sign methods
# (like groups.sub_X_Y_out):
sign_module_name = "groups."
stable = {
    "subgroup": {
        
        # order of args must be same as in
        # node args:

        # subgroup("[(1,2),(1,2,3)]", "Y", True)
        (True, False, True): {"func_name": "sub_x_Y_out",
                              "type": "rand", "count_of_samples": 10},

        # subgroup("X", "[(1,2), (1,2,3)]", True)
        (False, True, True): {"func_name": "sub_X_y_out",
                              "type": "rand", "count_of_samples": 10},

        # subgroup("[(1,2)]", "[(1,2), (1,2,3)]", "Out")
        (True, True, False): {"func_name": "sub_x_y_Out",
                              "type": "det"},

        # subgroup("[(1,2)]", "[(1,2), (1,2,3)]", "Out")
        (True, True, True): {"func_name": "sub_x_y_out",
                             "type": "det"}},
    "abelian": {

        # abelian("[(4,5), (1,2,3)]", "Out")
        (True, False): {"func_name": "abelian_x_Out",
                        "type": "det"},
        # abelian("[(4,5), (1,2,3)]", True)
        (True, True): {"func_name": "abelian_x_Out",
                       "type": "det"},

        # abelian("X", True)
        (False, True): {"func_name": "abelian_X_out",
                        "type": "rand", "count_of_samples": 3},
    },
    
    # all this below don't used now
    # (because they all determent and fixed):
    # just for compatibility:
    "conj": {
            (True, True, False): {"func_name": "conj_a0_a1_Out",
                                  "type": "det"},
            (False, True, True): {"func_name": "conj_A0_a1_out",
                                  "type": "det"},
            (True, False, True): {"func_name": "conj_a0_A1_out",
                                  "type": "det"},
            (False, False, True): {"func_name": "conj_A0_A1_out",
                                   "type": "rand"},
        },
    
    "if": {
            (True, True, False): {"func_name": "if_a0_a1_Out",
                                  "type": "det"},
            (False, True, True): {"func_name": "if_A0_a1_out",
                                  "type": "det"},
            (True, False, True): {"func_name": "if_a0_A1_out",
                                  "type": "det"},
            (False, False, True): {"func_name": "if_A0_A1_out",
                                   "type": "rand"},
        }}


stable_fixed = {
    # pred: (args values):
    "if": (True, True, True),
    "conj": (True, True, True),
}
