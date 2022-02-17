import os
import warnings

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from global_parameters import *
from utils import *


# todo: add documentation to all functions


def visualize_distance_metric_of_altering_flag_values_by_treatment(p_nuc_distance_by_treatment: dict,
                                                                   p_prop_distance_by_treatment: dict,
                                                                   flag_name: str, full_path_to_save_fig: str = None,
                                                                   **kwargs):
    plt.clf()
    distance_metric_name = kwargs.get('distance_metric_name', 'RMSE')
    visualize_specific_treatments = kwargs.get('visualize_specific_treatments', 'all')

    if visualize_specific_treatments != 'all' and type(visualize_specific_treatments) == type(list()):
        full_treatment_names = []
        for full_treatment_name in p_prop_distance_by_treatment.keys():
            for given_treatment_name in visualize_specific_treatments:
                if given_treatment_name.lower() in full_treatment_name.lower():
                    full_treatment_names.append(full_treatment_name)

        p_nuc_distance_by_treatment = {key: val for key, val in p_nuc_distance_by_treatment.items() if
                                       key in full_treatment_names}
        p_prop_distance_by_treatment = {key: val for key, val in p_prop_distance_by_treatment.items() if
                                        key in full_treatment_names}

    fig, ax = plt.subplots()
    treatments_axis = np.arange(0, len(p_nuc_distance_by_treatment), 1)
    ax.bar(x=treatments_axis, height=list(p_nuc_distance_by_treatment.values()), color=(1, 0, 0, .8),
           label='Fraction of Nucleators')
    ax.set_xticks(treatments_axis)
    ax.set_xticklabels(list(p_nuc_distance_by_treatment.keys()))
    ax.tick_params(axis='x', labelrotation=-45, labelsize=kwargs.get('x_tick_label_size', 8))
    ax.set_ylabel(f'{distance_metric_name} distance between {flag_name} results')
    ax.set_title('P(Nuc)')

    ax.bar(x=treatments_axis, height=list(p_prop_distance_by_treatment.values()), color=(0, 1, 1, .8),
           label='Fraction of Propagators')
    ax.set_xticks(treatments_axis)
    ax.set_xticklabels(list(p_prop_distance_by_treatment.keys()))
    ax.tick_params(axis='x', labelrotation=-45, labelsize=kwargs.get('x_tick_label_size', 8))
    ax.set_ylabel(f'{distance_metric_name} distance between {flag_name} results')
    ax.set_title('P(Prop)')

    ax.legend()
    plt.setp(ax.xaxis.get_majorticklabels(), ha="left", rotation_mode="anchor")
    plt.tight_layout()

    if SHOWFIG:
        plt.show()
    elif SAVEFIG:
        path_for_plot_dir = full_path_to_save_fig if full_path_to_save_fig is not None else \
            os.sep.join(
                os.getcwd().split(os.sep)[:-1] + ['Results', 'MeasurementsEndpointReadoutsPlots',
                                                  'Comparison_between_flags',
                                                  'Global_P_Nuc_VS_P_Prop'])
        if not os.path.isdir(path_for_plot_dir):
            os.makedirs(path_for_plot_dir)

        path_for_plot = os.sep.join([path_for_plot_dir,
                                     f'global_p_nuc_vs_p_prop_all_exps_flag={flag_name}_{distance_metric_name}_distance_scores'])

        plt.savefig(path_for_plot + '.png', dpi=200)
        plt.savefig(path_for_plot + '.eps', dpi=200)

    plt.close(fig)


def visualize_endpoint_readouts_by_treatment_to_varying_calculation_flags(xy1_readout_tuple: Tuple[np.array, np.array],
                                                                          treatment_per_readout1: np.array,
                                                                          xy2_readout_tuple: Tuple[np.array, np.array],
                                                                          treatment_per_readout2: np.array,
                                                                          full_path_to_save_fig: str = None,
                                                                          x_label: str = 'Fraction of Nucleators',
                                                                          y_label: str = 'Fraction of Propagators',
                                                                          use_log: bool = False,
                                                                          **kwargs):
    plt.clf()

    first_flag_value_color = kwargs.get('first_flag_value_color', (1, 0, 0, .5))
    second_flag_value_color = kwargs.get('second_flag_value_color', (0, 0, 1, .5))
    first_flag_type_name_and_value = kwargs.get('first_flag_type_name_and_value', 'Recent death=True')
    second_flag_type_name_and_value = kwargs.get('second_flag_type_name_and_value', 'Recent death=False')

    flag_name = first_flag_type_name_and_value.split('=')[0]

    if use_log:
        x1_readout = np.log10(xy1_readout_tuple[0])
        y1_readout = np.log10(xy1_readout_tuple[1])
        x2_readout = np.log10(xy2_readout_tuple[0])
        y2_readout = np.log10(xy2_readout_tuple[1])
    else:
        x1_readout = xy1_readout_tuple[0]
        y1_readout = xy1_readout_tuple[1]
        x2_readout = xy2_readout_tuple[0]
        y2_readout = xy2_readout_tuple[1]

    fig, ax = plt.subplots(figsize=(10, 10))
    marker1_per_point, color_per_point, treatment1_to_marker, treatment1_to_color = \
        get_marker_per_treatment_list(treatment_per_readout1)
    marker2_per_point, color_per_point, treatment2_to_marker, treatment2_to_color = \
        get_marker_per_treatment_list(treatment_per_readout2)

    # plotting the results of the first flag value
    for point_idx, xy in enumerate(zip(x1_readout, y1_readout)):
        x, y = xy
        marker = marker1_per_point[point_idx]
        # color = color_per_point[point_idx]
        # marker_size = 10 if 'tnf' in treatment_per_readout1[point_idx].lower() else 5
        ax.plot(x, y, marker=marker, color=first_flag_value_color,
                label=treatment_per_readout1[point_idx])  # ,ms=marker_size)

    # plotting the results of the second flag value
    for point_idx, xy in enumerate(zip(x2_readout, y2_readout)):
        x, y = xy
        marker = marker2_per_point[point_idx]
        # color = color_per_point[point_idx]
        # marker_size = 10 if 'tnf' in treatment_per_readout1[point_idx].lower() else 5
        ax.plot(x, y, marker=marker, color=second_flag_value_color,
                label=treatment_per_readout2[point_idx])  # ,ms=marker_size)

    custom_handles, custom_lables = \
        get_custom_legend_artists(labels_to_colors={key: 'black' for key in treatment1_to_color.keys()},
                                  labels_to_markers=treatment1_to_marker)

    lgd = ax.legend(handles=custom_handles, labels=custom_lables, loc='best', bbox_to_anchor=(1.05, 1))
    handles, labels = ax.get_legend_handles_labels()
    ax.grid('on')
    ax.set_xlabel('Log' + x_label if use_log else x_label)
    ax.set_ylabel('Log' + y_label if use_log else y_label)

    add_to_title = f'{first_flag_value_color} is {first_flag_type_name_and_value}\n{second_flag_value_color} is {second_flag_type_name_and_value}'
    ax.set_title(
        f'Log(Fraction) of Nucleators & Propagators\n{add_to_title}' if use_log else f'Fraction of Nucleators & Propagators\n{add_to_title}')

    if not use_log:
        ax.set_xticks([0.1, .30])
        ax.set_yticks([0.6, 0.95])
    else:
        ax.set_xticks([-1, 0])
        ax.set_yticks([-.4, 0])
    plt.tight_layout()

    if SHOWFIG:
        plt.show()
    elif SAVEFIG:
        path_for_plot_dir = full_path_to_save_fig if full_path_to_save_fig is not None else \
            os.sep.join(
                os.getcwd().split(os.sep)[:-1] + ['Results', 'MeasurementsEndpointReadoutsPlots',
                                                  'Comparison_between_flags',
                                                  'Global_P_Nuc_VS_P_Prop'])
        if not os.path.isdir(path_for_plot_dir):
            os.makedirs(path_for_plot_dir)

        if use_log:
            path_for_plot = os.sep.join(
                [path_for_plot_dir, f'LOG_global_p_nuc_vs_p_prop_all_exps_flag={flag_name}.png'])
        else:
            path_for_plot = os.sep.join([path_for_plot_dir, f'global_p_nuc_vs_p_prop_all_exps_flag={flag_name}.png'])
        plt.savefig(path_for_plot, dpi=200, bbox_extra_artists=[lgd], bbox_inches='tight')

    plt.close(fig)


def visualize_endpoint_readouts_by_treatment_about_readouts(x_readout: np.array,
                                                            y_readout: np.array,
                                                            treatment_per_readout: np.array,
                                                            full_dir_path_to_save_fig: str = None,
                                                            full_path_to_save_fig: str = None,
                                                            x_label: str = 'Fraction of Nucleators',
                                                            y_label: str = 'Fraction of Propagators',
                                                            fig_title: str = 'Fraction of Nucleators & Propagators',
                                                            fig_name_to_save: str = None,
                                                            use_log: bool = False,
                                                            plot_about_treatment: bool = False,
                                                            **kwargs):
    auto_axis_lim = kwargs.get('auto_axis_lim', False)
    set_y_lim = kwargs.get('set_y_lim', True)
    set_x_lim = kwargs.get('set_x_lim', True)
    show_legend = kwargs.get('show_legend', False)
    legend_font_size = kwargs.get('legend_font_size', 6)
    legend_marker_ration = kwargs.get('legend_marker_ration', 0.8)
    recent_death_flag = kwargs.get('only_recent_death_flag_for_neighbors_calc', RECENT_DEATH_ONLY_FLAG)

    if use_log:
        x_readout = np.log10(x_readout)
        y_readout = np.log10(y_readout)
    if plot_about_treatment:
        fig, axis = plt.subplots(1, 2)
        unique_treatments = set(treatment_per_readout)
        x_axis_dict = {treatment_name: idx for idx, treatment_name in enumerate(unique_treatments)}
        # x_axis = np.arange(0, len(x_readout), 1)
    else:
        fig, ax = plt.subplots()  # figsize=(10, 10))

    marker_per_point, color_per_point, treatment_to_marker, treatment_to_color = \
        get_marker_per_treatment_list(treatment_per_readout)

    for point_idx, xy in enumerate(zip(x_readout, y_readout)):
        x, y = xy
        marker = marker_per_point[point_idx]
        color = color_per_point[point_idx]
        treatment_name = treatment_per_readout[point_idx]
        marker_size = 10 if 'tnf' in treatment_name.lower() else 5

        if plot_about_treatment:
            treatment_idx = x_axis_dict[treatment_name]
            axis[0].plot(treatment_idx, x, ms=marker_size, marker=marker,
                         color=color, label=treatment_per_readout[point_idx])
            axis[1].plot(treatment_idx, y, ms=marker_size, marker=marker,
                         color=color, label=treatment_per_readout[point_idx])
        else:
            ax.plot(x, y, ms=marker_size, marker=marker,
                    color=color, label=treatment_per_readout[point_idx])

    if plot_about_treatment:
        # temporal_unit = 'Minutes' if temporal_resolution != 1 else 'Frame#'
        axis[0].grid('on')
        axis[0].set_xlabel(f'Treatment type')
        axis[0].set_title('Log ' + x_label if use_log else x_label)
        axis[1].grid('on')
        axis[1].set_xlabel(f'Treatment type')
        axis[1].set_title('Log ' + y_label if use_log else y_label)

        if not use_log:
            axis[0].set_xticks(np.arange(0, len(x_axis_dict), 1))
            axis[0].set_xticklabels(list(x_axis_dict.keys()))
            axis[0].tick_params(axis='x', labelrotation=-45, labelsize=kwargs.get('x_tick_label_size', 4))
            axis[1].set_xticks(np.arange(0, len(x_axis_dict), 1))
            axis[1].set_xticklabels(list(x_axis_dict.keys()))
            axis[1].tick_params(axis='x', labelrotation=-45, labelsize=kwargs.get('x_tick_label_size', 4))

        else:
            axis[0].set_xticks(np.arange(0, len(x_axis_dict), 1))
            axis[0].set_xticklabels(list(x_axis_dict.keys()))
            axis[0].tick_params(axis='x', labelrotation=-45, labelsize=kwargs.get('x_tick_label_size', 4))
            axis[1].set_xticks(np.arange(0, len(x_axis_dict), 1))
            axis[1].set_xticklabels(list(x_axis_dict.keys()))
            axis[1].tick_params(axis='x', labelrotation=-45, labelsize=kwargs.get('x_tick_label_size', 4))

        plt.setp(axis[0].xaxis.get_majorticklabels(), ha="left", rotation_mode="anchor")
        plt.setp(axis[1].xaxis.get_majorticklabels(), ha="left", rotation_mode="anchor")

        if not use_log:
            if recent_death_flag:
                y_tick_limits_x_label = [0.15, 0.6]
                y_tick_limits_y_label = [0.35, 0.9]
            else:
                y_tick_limits_x_label = [0.1, 0.3]
                y_tick_limits_y_label = [0.7, 0.95]
        else:
            if recent_death_flag:
                y_tick_limits_x_label = [-0.8, -0.2]
                y_tick_limits_y_label = [-0.4, 0]
            else:
                y_tick_limits_x_label = [-1, -0.5]
                y_tick_limits_y_label = [-0.2, 0]
        if set_y_lim and not auto_axis_lim:
            axis[0].set_ylim(y_tick_limits_x_label)
            axis[1].set_ylim(y_tick_limits_y_label)

    else:
        ax.grid('on')
        ax.set_xlabel('Log ' + x_label if use_log else x_label)
        ax.set_ylabel('Log ' + y_label if use_log else y_label)
        ax.set_title(fig_title if not use_log else f'Log of {fig_title}')
        if not use_log:
            x_tick_limits = [0, 0.30]
            y_tick_limits = [0.6, 0.95]
        else:
            x_tick_limits = [-1, 0]
            y_tick_limits = [-.4, 0]
        if set_y_lim and not auto_axis_lim:
            ax.set_xlim(x_tick_limits)
            ax.set_ylim(y_tick_limits)
    if not plot_about_treatment:
        if y_readout.max() <= .4 and not auto_axis_lim:
            ax.set_ylim([0, 0.4])
        elif y_readout.max() <= 1 and not auto_axis_lim:
            ax.set_ylim([0, 1])
        elif auto_axis_lim:
            ax.set_ylim((max((0, y_readout.min() - 0.01)), min((1.1, y_readout.max() + 0.01))))
            ax.set_xlim((max((0, x_readout.min() - 0.01)), max((1.1, x_readout.max() + 0.01))))
        if set_x_lim and not auto_axis_lim:
            if x_readout.max() <= .3:
                ax.set_xlim([0, 0.3])
            elif x_readout.max() <= .4:
                ax.set_xlim([0, 0.4])
            elif x_readout.max() <= 1:
                ax.set_xlim([0, 1])
            elif x_readout.max() >= 50:
                ax.set_xlim((0, 150))
            else:
                ax.set_xlim((max((0, x_readout.min())), min((1.1, x_readout.max()))))
    if show_legend:
        # filter treatments colors and markers to show only computed treatments in legend
        filtered_treatment_to_color = {}
        filtered_treatment_to_marker = {}
        for key, val in treatment_to_color.items():
            if key in treatment_per_readout:
                filtered_treatment_to_color[key] = val
                filtered_treatment_to_marker[key] = treatment_to_marker[key]

        custom_handles, custom_lables = get_custom_legend_artists(labels_to_colors=filtered_treatment_to_color,
                                                                  labels_to_markers=filtered_treatment_to_marker)

        plt.legend(handles=custom_handles,
                   labels=custom_lables,
                   loc='best',
                   fontsize=legend_font_size,
                   markerscale=legend_marker_ration)

    plt.tight_layout()

    if SHOWFIG:
        plt.show()
    elif SAVEFIG:
        if recent_death_flag:
            path_for_plot_dir = full_dir_path_to_save_fig if full_dir_path_to_save_fig is not None else \
                os.sep.join(
                    os.getcwd().split(os.sep)[:-1] + ['Results', 'MeasurementsEndpointReadoutsPlots',
                                                      'Only recent death considered for neighbors results',
                                                      'Global_P_Nuc_VS_P_Prop'])
        else:
            path_for_plot_dir = full_dir_path_to_save_fig if full_dir_path_to_save_fig is not None else os.sep.join(
                os.getcwd().split(os.sep)[:-1] + ['Results', 'MeasurementsEndpointReadoutsPlots',
                                                  'Global_P_Nuc_VS_P_Prop'])
        if not os.path.isdir(path_for_plot_dir):
            os.makedirs(path_for_plot_dir)

        if fig_name_to_save is None:
            plot_about_time_path_addition = '_about_treatment' if plot_about_treatment else ''
            if use_log:
                path_for_plot = os.sep.join(
                    [path_for_plot_dir, f'LOG_global_p_nuc_vs_p_prop_all_exps{plot_about_time_path_addition}'])
            else:
                path_for_plot = os.sep.join(
                    [path_for_plot_dir, f'global_p_nuc_vs_p_prop_all_exps{plot_about_time_path_addition}'])
        else:
            path_for_plot = os.sep.join([path_for_plot_dir, fig_name_to_save])

        path_for_plot = path_for_plot if full_path_to_save_fig is None else full_path_to_save_fig
        plt.savefig(path_for_plot + '.png', dpi=200)  # , bbox_extra_artists=[lgd], bbox_inches='tight')
        plt.savefig(path_for_plot + '.eps', dpi=200)  # , bbox_extra_artists=[lgd], bbox_inches='tight')

    plt.close(fig)


def visualize_endpoint_readouts_by_treatment_about_readouts_3d(x_readout: np.array,
                                                               y_readout: np.array,
                                                               z_readout: np.array,
                                                               treatment_per_readout: np.array,
                                                               full_dir_path_to_save_fig: str = None,
                                                               fig_name_to_save: str = None,
                                                               full_path_to_save_fig: str = None,
                                                               x_label: str = 'Fraction of Nucleators',
                                                               y_label: str = 'Fraction of Propagators',
                                                               z_label: str = 'Experiment Density',
                                                               fig_title: str = 'Fraction of Nucleators & Propagators',
                                                               **kwargs):
    show_legend = kwargs.get('show_legend', False)
    legend_font_size = kwargs.get('legend_font_size', 6)
    legend_marker_ration = kwargs.get('legend_marker_ration', 0.8)

    marker_per_point, color_per_point, treatment_to_marker, treatment_to_color = \
        get_marker_per_treatment_list(treatment_per_readout)

    fig = plt.figure()

    ax = fig.add_subplot(projection='3d')

    for point_idx, coordinates in enumerate(zip(x_readout, y_readout, z_readout)):
        px, py, pz = coordinates

        color, marker = color_per_point[point_idx], marker_per_point[point_idx]
        ax.scatter(px, py, pz, marker=marker, color=color)

    ax.set_ylim([0, 1])
    ax.set_xlim([0, 1])

    ax.grid('on')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_zlabel(z_label)
    ax.set_title(fig_title)

    if show_legend:
        # filter treatments colors and markers to show only computed treatments in legend
        filtered_treatment_to_color = {}
        filtered_treatment_to_marker = {}
        for key, val in treatment_to_color.items():
            if key in treatment_per_readout:
                filtered_treatment_to_color[key] = val
                filtered_treatment_to_marker[key] = treatment_to_marker[key]

        custom_handles, custom_labels = get_custom_legend_artists(labels_to_colors=filtered_treatment_to_color,
                                                                  labels_to_markers=filtered_treatment_to_marker)

        plt.legend(handles=custom_handles,
                   labels=custom_labels,
                   loc='best',
                   fontsize=legend_font_size,
                   markerscale=legend_marker_ration)

    plt.tight_layout()

    if SHOWFIG:
        plt.show()
    elif SAVEFIG:
        path_for_plot_dir = full_dir_path_to_save_fig if full_dir_path_to_save_fig is not None else os.sep.join(
            os.getcwd().split(os.sep)[:-1] + ['Results', 'MeasurementsEndpointReadoutsPlots',
                                              'Global_P_Nuc_VS_P_Prop'])

        if not os.path.isdir(path_for_plot_dir):
            os.makedirs(path_for_plot_dir)

        if fig_name_to_save is None:
            plot_about_time_path_addition = '_about_treatment' if plot_about_treatment else ''
            path_for_plot = os.sep.join(
                [path_for_plot_dir, f'global_p_nuc_vs_p_prop_all_exps{plot_about_time_path_addition}'])
        else:
            path_for_plot = os.sep.join([path_for_plot_dir, fig_name_to_save])

        path_for_plot = path_for_plot if full_path_to_save_fig is None else full_path_to_save_fig
        plt.savefig(path_for_plot + '.png', dpi=200)  # , bbox_extra_artists=[lgd], bbox_inches='tight')
        plt.savefig(path_for_plot + '.eps', dpi=200)  # , bbox_extra_artists=[lgd], bbox_inches='tight')

    plt.close(fig)


def visualize_cell_death_in_time(xyt_df: pd.DataFrame = None,
                                 xyt_full_path: str = None,
                                 nucleators_mask: np.array = None,
                                 propagators_maks: np.array = None,
                                 full_path_to_save_fig: str = None,
                                 exp_treatment: str = None, exp_name: str = None) -> None:
    """

    :param xyt_df:
    :param xyt_full_path:
    :param nucleators_mask:
    :param full_path_to_save_fig:
    :param exp_treatment:
    :param exp_name:
    :return:
    """
    plt.clf()

    if xyt_df is None and xyt_full_path is None:
        raise ValueError('either df or path must be not None!')

    if exp_treatment is None or exp_name is None:
        raise ValueError('must provide exp treatment and name!')

    # clean exp_name and treatment from bad characters
    exp_name, exp_treatment = clean_string_from_bad_chars(exp_treatment, replacement=''), clean_string_from_bad_chars(
        exp_treatment)

    data = xyt_df if xyt_df is not None else pd.read_csv(xyt_full_path)
    death_times = data['death_time'].values
    x, y = data['cell_x'].values, data['cell_y'].values

    min_time_of_death, max_time_of_death = death_times.min(), death_times.max()
    fig, ax = plt.subplots()

    cmap = mpl.cm.__builtin_cmaps[12]
    ax.scatter(x, y, c=death_times, cmap=cmap)

    # mark nucleators
    if nucleators_mask is not None:
        nucleators_indices = np.where(nucleators_mask)[0]
        ax.scatter(x[(nucleators_indices)], y[(nucleators_indices)], marker='x', color=(0, 1, 0, .5))
    # mark propagators
    if propagators_maks is not None:
        propagators_indices = np.where(propagators_maks)[0]
        ax.scatter(x[(propagators_indices)], y[(propagators_indices)], marker='+', color=(1, 0, 1, .5))

    ax.set_xticks([])
    ax.set_yticks([])
    # colorbar
    norm = mpl.colors.Normalize(vmin=min_time_of_death, vmax=max_time_of_death)
    plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, label='time of death')

    plt.tight_layout()

    if SHOWFIG:
        plt.show()
    elif SAVEFIG:
        if RECENT_DEATH_ONLY_FLAG:
            path_for_plot_dir = full_path_to_save_fig if full_path_to_save_fig is not None else \
                os.sep.join(
                    os.getcwd().split(os.sep)[:-1] + ['Results', 'CellDeathVisualizations',
                                                      'Only recent death considered for neighbors results',
                                                      f'{exp_treatment}'])
        else:
            path_for_plot_dir = full_path_to_save_fig if full_path_to_save_fig is not None else os.sep.join(
                os.getcwd().split(os.sep)[:-1] + ['Results', 'CellDeathVisualizations', f'{exp_treatment}'])
        if not os.path.isdir(path_for_plot_dir):
            os.makedirs(path_for_plot_dir)

        path_for_plot = os.sep.join([path_for_plot_dir, f'{exp_name}.png'])
        plt.savefig(path_for_plot, dpi=200)
        path_for_plot = os.sep.join([path_for_plot_dir, f'{exp_name}.eps'])
        plt.savefig(path_for_plot, dpi=200)

    plt.close(fig)


def plot_measurements_by_time(measurement1_by_time: np.array,
                              measurement2_by_time: np.array = None,
                              measurement3_by_time: np.array = None,
                              temporal_resolution: int = None,
                              exp_name: str = None, exp_treatment: str = None,
                              full_path_to_save_fig: str = None,
                              max_time: int = None) -> None:
    """

    :param measurement1_by_time:
    :param measurement2_by_time:
    :param measurement3_by_time:
    :param temporal_resolution:
    :param exp_name:
    :param exp_treatment:
    :param full_path_to_save_fig:
    :return:
    """
    if temporal_resolution is None:
        raise ValueError('temporal resolution can not be None!')

    plt.clf()

    # clean exp_name and treatment from bad characters
    exp_name, exp_treatment = clean_string_from_bad_chars(exp_name, replacement=''), clean_string_from_bad_chars(
        exp_treatment)

    max_time = len(measurement1_by_time) * temporal_resolution if max_time is None else max_time
    time_axis = np.arange(0, max_time + 1, temporal_resolution)

    fig, ax = plt.subplots()

    ax.set_title(f'Treatment: {exp_treatment}\nexp:{exp_name}')

    ax1_clr = 'tab:blue'
    ax.plot(time_axis, measurement1_by_time, label='Nucleation')
    ax.set_ylabel('P(Nuc)', color=ax1_clr)

    ax.tick_params(axis='y', labelcolor=ax1_clr)
    ax.set_ylim(0, 1)
    ax.set_xticks([time_axis[0], time_axis[len(time_axis) // 2], time_axis[-1]])
    # ax.set_xticklabels(['{}-{}'.format(x, x + 100) for x in time_ticks])
    if measurement2_by_time is not None:
        ax2_color = 'tab:red'
        ax2 = ax.twinx()
        ax2.plot(time_axis, measurement2_by_time, label='Propagation', color=ax2_color)
        ax2.set_ylabel('P(Prop)', color=ax2_color)
        ax2.tick_params(axis='y', labelcolor=ax2_color)
        ax2.set_ylim(0, 1)
        # plotting accumulated death
        ax.set_xlabel('Time Window (Minutes)')
    if measurement3_by_time is not None:
        ax.plot(time_axis, measurement3_by_time, label='Accumulated Death', color='black', marker='p')

        # plot lines to visualize 10%-90% cells deaths
        tenth_percentile = np.where(measurement3_by_time >= .1)[0][0]
        plt.axvline(x=time_axis[tenth_percentile], c='black', linestyle='--', linewidth=0.7)

        nineteenth_percentile = np.where(measurement3_by_time >= .9)[0][0]
        plt.axvline(x=time_axis[nineteenth_percentile], c='black', linestyle='--', linewidth=0.7)

    plt.tight_layout()

    if SHOWFIG:
        plt.show()
    elif SAVEFIG:
        if RECENT_DEATH_ONLY_FLAG:
            path_for_plot_dir = full_path_to_save_fig if full_path_to_save_fig is not None else \
                os.sep.join(
                    os.getcwd().split(os.sep)[:-1] + ['Results', 'TemporalMeasurementsPlots',
                                                      'Only recent death considered for neighbors results',
                                                      f'{exp_treatment}'])
        else:
            path_for_plot_dir = full_path_to_save_fig if full_path_to_save_fig is not None else \
                os.sep.join(
                    os.getcwd().split(os.sep)[:-1] + ['Results', 'TemporalMeasurementsPlots', f'{exp_treatment}'])
        if not os.path.isdir(path_for_plot_dir):
            os.makedirs(path_for_plot_dir)

        path_for_plot = os.sep.join([path_for_plot_dir, f'{exp_name}'])
        plt.savefig(path_for_plot + '.png', dpi=200)
        plt.savefig(path_for_plot + '.eps', dpi=200)

    plt.close(fig)


def scatter_with_linear_regression_line(x: np.array, y: np.array, x_label: str, y_label: str, title: str,
                                        path_to_save_fig: str, plot_linear_regression: bool = False,
                                        color_map: dict = None, colors: np.array = None, **kwargs):
    """

    :param colors:
    :param color_map:
    :param plot_linear_regression:
    :param x:
    :param y:
    :param x_label:
    :param y_label:
    :param title:
    :param path_to_save_fig:
    :return:
    """
    plt.clf()

    marker_size = kwargs.get('marker_size', 300)
    fig, ax = plt.subplots()
    # plot probabilities for each level of neighborhoods
    if color_map is None or colors is None:
        ax.scatter(x, y, s=marker_size, color=(0, 1, 0, 0.8), marker='*')
    else:
        ax.scatter(x, y, s=marker_size, marker='*', c=colors, cmap=color_map)

    if plot_linear_regression:
        # plot linear regression line
        regression_line_x, regression_line_y = get_linear_regression_line_between_two_signals(x, y)
        ax.plot(regression_line_x, regression_line_y)
    else:
        regression_line = np.linspace(0, 1, num=len(x), endpoint=True)
        ax.plot(regression_line, regression_line)
    # plot decoration
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)

    ax.set_ylim((0, 1))
    ax.set_xlim((0, 1))

    if colors is not None and color_map is not None:
        norm = mpl.colors.Normalize(vmin=colors.min(), vmax=colors.max())
        plt.colorbar(cm.ScalarMappable(norm=norm, cmap=color_map), ax=ax, label='time of death')

    plt.tight_layout()

    if SAVEFIG:
        plt.savefig(f'{path_to_save_fig}.png', dpi=200)
        plt.savefig(f'{path_to_save_fig}.eps', dpi=200)
    elif SHOWFIG:
        plt.show()
    plt.close(fig=fig)


def scatter_with_linear_regression_line_about_treatment(x_readout: np.array, y_readout: np.array, x_label: str,
                                                        y_label: str, title: str,
                                                        path_to_save_fig: str = '',
                                                        plot_linear_regression: bool = False,
                                                        exps_treatments: np.array = None, **kwargs):
    """

    :param colors:
    :param color_map:
    :param plot_linear_regression:
    :param x:
    :param y:
    :param x_label:
    :param y_label:
    :param title:
    :param path_to_save_fig:
    :return:
    """
    plt.clf()

    marker_size = kwargs.get('marker_size', 300)
    legend_font_size = kwargs.get('legend_font_size', 6)
    legend_marker_ration = kwargs.get('legend_marker_ration', 0.8)


    marker_per_point, color_per_point, treatment_to_marker, treatment_to_color = \
        get_marker_per_treatment_list(exps_treatments)

    fig, ax = plt.subplots()
    # plot probabilities for each level of neighborhoods
    for point_idx, xyt in enumerate(zip(x_readout, y_readout, exps_treatments)):
        x, y, exp_treatment = xyt
        treatment_color, treatment_marker = treatment_to_color[exp_treatment], treatment_to_marker[exp_treatment]
        ax.scatter(x, y, s=marker_size, color=treatment_color, marker=treatment_marker)

    if plot_linear_regression:
        # plot linear regression line
        regression_line_x, regression_line_y = get_linear_regression_line_between_two_signals(x_readout, y_readout)
        ax.plot(regression_line_x, regression_line_y)
    else:
        regression_line = np.linspace(0, 1, num=len(x_readout), endpoint=True)
        ax.plot(regression_line, regression_line)

    # plot labels
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)

    filtered_treatment_to_color = {}
    filtered_treatment_to_marker = {}
    for key, val in treatment_to_color.items():
        if key in exps_treatments:
            filtered_treatment_to_color[key] = val
            filtered_treatment_to_marker[key] = treatment_to_marker[key]

    custom_handles, custom_labels = get_custom_legend_artists(labels_to_colors=filtered_treatment_to_color,
                                                              labels_to_markers=filtered_treatment_to_marker)

    plt.legend(handles=custom_handles,
               labels=custom_labels,
               loc='best',
               fontsize=legend_font_size,
               markerscale=legend_marker_ration)

    ax.set_ylim((0, 1))
    ax.set_xlim((0, 1))

    plt.tight_layout()

    if SAVEFIG:
        plt.savefig(f'{path_to_save_fig}.png', dpi=200)
        plt.savefig(f'{path_to_save_fig}.eps', dpi=200)
    elif SHOWFIG:
        plt.show()
    plt.close(fig=fig)


def plot_endpoint_readout_for_compressed_temporal_resolution(temporal_resolution_axis: np.array,
                                                             endpoint_readouts_values_p_nuc: np.array,
                                                             endpoint_readouts_values_p_prop: np.array,
                                                             exp_treatment: str,
                                                             exp_name: str,
                                                             full_path_to_save_fig: str = None,
                                                             **kwargs):
    fig, axis = plt.subplots(1, 2)
    fig.suptitle(f'Experiment:{exp_name}\nTreatment{exp_treatment}')
    x_axis = np.arange(0, len(temporal_resolution_axis), 1)
    axis[0].scatter(x_axis, endpoint_readouts_values_p_nuc)
    axis[0].set_xticks(x_axis)
    axis[0].set_xticklabels([f'{x}' for x in temporal_resolution_axis])
    axis[0].set_xlabel('Temporal resolution (Minutes)')
    axis[0].set_ylabel('Fraction of Nucleators')
    axis[0].set_ylim((0, 1))

    axis[1].scatter(x_axis, endpoint_readouts_values_p_prop)
    axis[1].set_xticks(x_axis)
    axis[1].set_xticklabels([f'{x}' for x in temporal_resolution_axis])
    axis[1].set_xlabel('Temporal resolution (Minutes)')
    axis[1].set_ylabel('Fraction of Propagators')
    axis[1].set_ylim((0, 1))

    plt.tight_layout()

    if SHOWFIG:
        plt.show()
    elif SAVEFIG:
        exp_treatment = clean_string_from_bad_chars(exp_treatment)
        recent_death_only = kwargs.get('only_recent_death_flag_for_neighbors_calc', RECENT_DEATH_ONLY_FLAG)
        if recent_death_only:
            path_for_plot_dir = full_path_to_save_fig if full_path_to_save_fig is not None else \
                os.sep.join(
                    os.getcwd().split(os.sep)[:-1] + ['Results',
                                                      'Compressed_MeasurementsEndpointReadoutsPlots',
                                                      'Only recent death considered for neighbors results',
                                                      'SingleExperimentsCompressionComparisons',
                                                      f'{exp_treatment}'])
        else:
            path_for_plot_dir = full_path_to_save_fig if full_path_to_save_fig is not None else \
                os.sep.join(
                    os.getcwd().split(os.sep)[:-1] + ['Results',
                                                      'Compressed_MeasurementsEndpointReadoutsPlots',
                                                      'SingleExperimentsCompressionComparisons',
                                                      f'{exp_treatment}'])
        if not os.path.isdir(path_for_plot_dir):
            os.makedirs(path_for_plot_dir)

        path_for_plot = os.sep.join([path_for_plot_dir, f'{exp_name}'])
        plt.savefig(f'{path_for_plot}.png', dpi=200)
        plt.savefig(f'{path_for_plot}.eps', dpi=200)

    plt.close(fig)


def plot_temporal_readout_for_entire_treatment(readouts: List[np.array],
                                               labels: List[str],
                                               treatment: str,
                                               unit_of_time: int,
                                               **kwargs) -> None:
    treatment = clean_string_from_bad_chars(treatment_name=treatment)
    only_consider_recent = kwargs.get('only_recent_death_flag_for_neighbors_calc',
                                      RECENT_DEATH_ONLY_FLAG)
    path_to_dir_to_save = kwargs.get('dir_path', os.sep.join(
        os.getcwd().split(os.sep)[:-1] + ['Results', 'TemporalMeasurementsPlots',
                                          'Only recent death considered for neighbors results',
                                          f'{treatment}']) if only_consider_recent else os.sep.join(
        os.getcwd().split(os.sep)[:-1] + ['Results', 'TemporalMeasurementsPlots',
                                          f'{treatment}']))
    fig_name = kwargs.get('fig_name', f'{treatment}_measurements_per_{unit_of_time}_min')

    fig, axis = plt.subplots(1, 2)

    colors = kwargs.get('colors_map', ['red', 'blue'])

    for ax_idx, ax in enumerate(axis):

        label = labels[ax_idx]
        color = colors[ax_idx]
        for treatment_readouts in readouts:
            readout = treatment_readouts[ax_idx]
            time_axis = np.arange(0, len(readout) * unit_of_time, unit_of_time)
            ax.plot(time_axis, readout, c=color)

        ax.set_xticks([time_axis[0]] + [time_axis[-1]])
        ax.set_title(label)
    fig.suptitle(f'{treatment} Treated')
    if SHOWFIG:
        plt.show()
    elif SAVEFIG:
        if not os.path.isdir(path_to_dir_to_save):
            os.makedirs(path_to_dir_to_save)

        full_path = os.sep.join([path_to_dir_to_save, fig_name])
        plt.savefig(f'{full_path}.png', dpi=200)
        plt.savefig(f'{full_path}.eps', dpi=200)


def visualize_histogram_of_values(
        hist_values: np.array,
        title: str,
        x_label: str,
        y_label: str,
        x_tick_labels: List[str] = None,
        path_to_dir_to_save: str = None,
        fig_name: str = None,
        **kwargs
):
    """
    histogram values must be pre-computed before invoking this function as it does not call
    plt.hist but plt.bar .
    :param hist_values:
    :param title:
    :param x_label:
    :param y_label:
    :param x_ticks:
    :param x_tick_labels:
    :param path_to_dir_to_save:
    :param fig_name:
    :return:
    """
    plt.clf()

    fig, ax = plt.subplots()

    if x_tick_labels is not None:
        ax.bar(np.arange(0, len(hist_values), 1), hist_values)
        ax.set_xticks(np.arange(0, len(hist_values), 1))
        ax.set_xticklabels(x_tick_labels)
        ax.tick_params(axis='x', labelrotation=-45, labelsize=kwargs.get('x_tick_label_size', 8))
    else:
        ax.bar(np.arange(0, len(hist_values), 1), hist_values)

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    plt.tight_layout()

    if SHOWFIG:
        plt.show()
    elif SAVEFIG:
        if not os.path.isdir(path_to_dir_to_save):
            os.makedirs(path_to_dir_to_save)

        full_path = os.sep.join([path_to_dir_to_save, fig_name])
        plt.savefig(f'{full_path}.png', dpi=200)
        plt.savefig(f'{full_path}.eps', dpi=200)

    plt.close(fig)


def present_fig(fig: plt.figure,
                ax: plt.axis,
                measurement_type: str,
                save_fig: bool = None,
                show_fig: bool = None,
                full_dir_path_to_save_fig: str = None,
                fig_name_suffix: str = '',
                fig_name_prefix: str = '') -> None:
    if show_fig is None:
        show_fig = SHOWFIG
    if save_fig is None:
        save_fig = SAVEFIG

    if show_fig:
        plt.show()
    elif save_fig:
        path_for_plot_dir = full_dir_path_to_save_fig if full_dir_path_to_save_fig is not None else os.sep.join(
            os.getcwd().split(os.sep)[:-1] + ['Results', 'MeasurementsEndpointReadoutsPlots'])
        if not os.path.isdir(path_for_plot_dir):
            os.makedirs(path_for_plot_dir)

        path_for_plot = os.sep.join(
            [path_for_plot_dir, f'{fig_name_prefix}_{measurement_type}_{fig_name_suffix}_about_treatment'])

        fig.savefig(path_for_plot + '.png', dpi=200)  # , bbox_extra_artists=[lgd], bbox_inches='tight')
        fig.savefig(path_for_plot + '.eps', dpi=200)  # , bbox_extra_artists=[lgd], bbox_inches='tight')


def visualize_measurement_per_treatment(readouts_per_experiment: np.array,
                                        treatment_name_per_readout: np.array,
                                        x_label: str,
                                        y_label: str,
                                        measurement_type: str,
                                        dir_to_save_fig_full_path: str,
                                        **kwargs) -> None:
    # set_y_lim = kwargs.get('set_y_lim', True)
    save_fig = kwargs.get('save_fig', SAVEFIG)
    show_fig = kwargs.get('show_fig', SHOWFIG)

    fig_name_suffix = kwargs.get('fig_name_suffix', '')
    fig_name_prefix = kwargs.get('fig_name_prefix', '')

    marker_per_point, color_per_point, treatment_to_marker, treatment_to_color = \
        get_marker_per_treatment_list(treatment_name_per_readout)

    unique_treatment_names = np.unique(treatment_name_per_readout)
    unique_treatment_names_to_idx = {treatment_name: idx for idx, treatment_name in enumerate(unique_treatment_names)}
    treatment_idx_for_experiment = np.array([unique_treatment_names_to_idx[treatment_name]
                                             for treatment_name in treatment_name_per_readout])

    plt.clf()

    fig, ax = plt.subplots()
    for xp, yp, m, c in zip(treatment_idx_for_experiment, readouts_per_experiment, marker_per_point, color_per_point):
        ax.scatter([xp], [yp], marker=m, color=c)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_xticks(np.arange(0, len(unique_treatment_names), 1))
    ax.set_xticklabels(unique_treatment_names)
    ax.tick_params(axis='x', labelrotation=-45, labelsize=kwargs.get('x_tick_label_size', 8))

    plt.setp(ax.xaxis.get_majorticklabels(), ha="left", rotation_mode="anchor")
    plt.tight_layout()

    present_fig(fig, ax,
                measurement_type=measurement_type,
                save_fig=save_fig,
                show_fig=show_fig,
                full_dir_path_to_save_fig=dir_to_save_fig_full_path,
                fig_name_suffix=fig_name_suffix,
                fig_name_prefix=fig_name_prefix)

    plt.close(fig)


def plot_multiple_experiments_temporal_readouts(experiments_readouts: List[Dict[str, Union[str, np.array]]],
                                                fig_x_label: str,
                                                fig_y_label: str,
                                                fig_title: str,
                                                dir_to_save_fig_full_path: str,
                                                measurement_type: str,
                                                **kwargs) -> None:
    """
    each element in experiments_readouts list is a dictionary with the following keys-values:
        'exp_name' - OPTIONAL[str], the name that will appear in the legend of the plot, if not provided,
            no legend will be rendered.
        'x_readout' - np.array size N
        'y_readout' - np.array size N
        'color_map' - OPTIONAL[np.array] size N, the color for each datapoint, if not provided, identical colors will
            be used for each experiment and no color bar will be rendered.
        'marker' - OPTIONAL[str], the marker to use when plotting the experiment, if not provided, the experiment will
            use the standart 'o' marker
        'plot_kwargs' - OPTIONAL[Dict], any additional key word arguments to pass to the ax.scatter method.

    :param fig_name_prefix:
    :param fig_name_suffix:
    :param measurement_type:
    :param experiments_readouts:
    :param fig_x_label:
    :param fig_y_label:
    :param fig_title:
    :param dir_to_save_fig_full_path:
    :param kwargs:
    :return:
    """

    # set_y_lim = kwargs.get('set_y_lim', True)
    save_fig = kwargs.get('save_fig', SAVEFIG)
    show_fig = kwargs.get('show_fig', SHOWFIG)

    fig_name_suffix = kwargs.get('fig_name_suffix', '')
    fig_name_prefix = kwargs.get('fig_name_prefix', '')
    color_bar_label = kwargs.get('color_bar_label', 'Normalized #neighbors')

    use_clr_map = True
    exp_min_value, exp_max_value = float('inf'), float('-inf')
    cmap = mpl.cm.__builtin_cmaps[12]
    use_legend = True

    fig, ax = plt.subplots()

    ax.set_xlabel(fig_x_label)
    ax.set_ylabel(fig_y_label)
    ax.set_title(fig_title)

    for experiment_idx, experiment_readouts_dict in enumerate(experiments_readouts):
        exp_name = experiment_readouts_dict.get('exp_name', '')
        exp_x_readout = experiment_readouts_dict.get('x_readout', None)
        exp_y_readout = experiment_readouts_dict.get('y_readout', None)
        exp_color_map = experiment_readouts_dict.get('color_map', None)
        exp_marker = experiment_readouts_dict.get('marker', 'o')
        exp_plot_kwarg = experiment_readouts_dict.get('plot_kwargs', {})

        if exp_x_readout is None or exp_y_readout is None:
            raise ValueError('Must provide x readouts and y readouts for each experiment!')

        # make sure we don't use color map and legend
        if exp_name == '':
            use_legend = False
        if exp_color_map is None:
            use_clr_map = False

        if use_clr_map:
            exp_min_value = exp_color_map.min() if exp_color_map.min() < exp_min_value else exp_min_value
            exp_max_value = exp_color_map.max() if exp_color_map.max() > exp_max_value else exp_max_value

            exp_plot_kwarg.pop('color', None)
            if use_legend:
                ax.scatter(exp_x_readout, exp_y_readout, marker=exp_marker, c=exp_color_map, cmap=cmap, label=exp_name,
                           **exp_plot_kwarg)
            else:
                ax.scatter(exp_x_readout, exp_y_readout, marker=exp_marker, c=exp_color_map, cmap=cmap,
                           **exp_plot_kwarg)
        else:
            if use_legend:
                ax.scatter(exp_x_readout, exp_y_readout, marker=exp_marker, label=exp_name, **exp_plot_kwarg)
            else:
                ax.scatter(exp_x_readout, exp_y_readout, marker=exp_marker, **exp_plot_kwarg)

    plt.tight_layout()

    if use_legend:
        plt.legend()
    if use_clr_map:
        norm = mpl.colors.Normalize(vmin=exp_min_value, vmax=exp_max_value)
        plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, label=color_bar_label)

    present_fig(fig, ax,
                measurement_type=measurement_type,
                save_fig=save_fig,
                show_fig=show_fig,
                full_dir_path_to_save_fig=dir_to_save_fig_full_path,
                fig_name_suffix=fig_name_suffix,
                fig_name_prefix=fig_name_prefix)

    plt.close(fig)
