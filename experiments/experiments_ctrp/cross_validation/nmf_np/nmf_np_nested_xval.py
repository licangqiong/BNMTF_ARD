"""
Run the nested cross-validation for the NP NMF class, on the CTRP dataset.
"""

import sys, os
project_location = os.path.dirname(__file__)+"/../../../../../"
sys.path.append(project_location)

from BNMTF_ARD.code.models.nmf_np import nmf_np
from BNMTF_ARD.code.cross_validation.nested_matrix_cross_validation import MatrixNestedCrossValidation
from BNMTF_ARD.data.drug_sensitivity.load_data import load_ctrp_ec50


''' Settings NMF. '''
train_config = {
    'iterations' : 500,
    'init_UV' : 'exponential',
    'expo_prior' : 0.1
}
predict_config = {}


''' Settings nested cross-validation. '''
K_range = [1,2,3,4]
no_folds = 10
no_threads = 5
parallel = False
output_file = "./results.txt"
files_nested_performances = ["./fold_%s.txt" % fold for fold in range(1,no_folds+1)]


''' Construct the parameter search. '''
parameter_search = [{'K':K} for K in K_range]


''' Load in the dataset. '''
R, M = load_ctrp_ec50()


''' Run the cross-validation framework. '''
nested_crossval = MatrixNestedCrossValidation(
    method=nmf_np,
    R=R,
    M=M,
    K=no_folds,
    P=no_threads,
    parameter_search=parameter_search,
    train_config=train_config,
    predict_config=predict_config,
    file_performance=output_file,
    files_nested_performances=files_nested_performances,
)
nested_crossval.run(parallel=parallel)
