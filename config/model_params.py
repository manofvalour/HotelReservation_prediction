from scipy.stats import randint, uniform

RF_PARAMS = {
    'n_estimators' : randint(50,500) ,
    'max_depth' : randint(5,50),
    'min_samples_split' : randint(2,15) ,
    'min_samples_leaf' : randint(1,10),
    'bootstrap' : [True, False]
}

RANDOM_SEARCH_PARAMS = {
    'n_iter': 4,
    'cv': 2,
    'n_jobs': -1,
    'verbose':2,
    'random_state': 42,
    'scoring': 'accuracy'
}

