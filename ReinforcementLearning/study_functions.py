import pickle

from optuna.visualization import plot_optimization_history, plot_param_importances, plot_contour, plot_edf, plot_slice, \
    plot_parallel_coordinate, plot_intermediate_values


def save_study(study, study_file_path, df_file_path):
    # Write report
    study.trials_dataframe().to_csv(df_file_path)

    with open(study_file_path, "wb+") as f:
        pickle.dump(study, f)


def plot_all(study):
    fig1 = plot_optimization_history(study)
    fig2 = plot_param_importances(study)
    fig3 = plot_contour(study)
    fig4 = plot_edf(study)
    fig5 = plot_slice(study)
    # fig6 = plot_pareto_front(study)
    fig7 = plot_parallel_coordinate(study)
    fig8 = plot_intermediate_values(study)

    fig1.show()
    fig2.show()
    fig3.show()
    fig4.show()
    fig5.show()
    # fig6.show()
    fig7.show()
    fig8.show()
