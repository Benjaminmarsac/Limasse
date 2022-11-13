import pandas as pd
import numpy as np
from PyQt5.QtWidgets import (QFileDialog, QErrorMessage)
import os
FULL_PATH = os.path.realpath(os.path.dirname(__file__))


def get_folder(folder: str):
    path = f"{FULL_PATH}/{folder}/"
    files_names = [f for f in os.listdir(path) if os.path.isfile(
        os.path.join(path, f)) if f.split(".")[-1] in ["csv"]]
    files_visu = [i.split(".")[0] for i in files_names]

    return files_names, files_visu


def open_filter(button_response: str, files_names: str, folder: str):
    if f"{button_response}.csv" in files_names:
        try:
            df = pd.read_csv(
                f"{FULL_PATH}/{folder}/{button_response}.csv", delimiter=",")
        except pd.errors.EmptyDataError:
            err = "Your filter is empty or doesn't\nstart on the right cell."
            return err
        if len(df.columns) > 1:
            return df
        elif len(df.columns) == 1:
            err = "Your csv is set on a wrong delimiter.\nYou should set it on ','"
            return err
    else:
        return "there's a problem"


def header_normalizer(df: pd.DataFrame):
    normalized = df.columns.to_list()
    normalized = [i.lower().strip() for i in normalized]
    df.columns = normalized

    return df


def placement(lateral_space, height_placement, height):
    position = lateral_space*height_placement+height*(height_placement-1)

    return int(position)


def save_data(excel_output: str, df: pd.DataFrame, sheet_name: str, header: list | None = None, mode: str = "w"):
    with pd.ExcelWriter(excel_output, mode=mode, engine="openpyxl") as written:
        df.to_excel(written, sheet_name, header=header)


def check_save(file: str, df: pd.DataFrame, sheet: str, count: int = 0):
    if count == 0:
        save_data(file, df, sheet, header=df.columns.to_list(), mode="w")
    else:
        save_data(file, df, sheet, header=df.columns.to_list(), mode="a")


def get_save_file(self: object):
    file_filter = 'Data File (*.xlsx *.csv *.dat);; Excel File (*.xlsx *.xls)'
    response = QFileDialog.getSaveFileName(
        parent=self,
        caption='Select a data file',
        directory='Data File.dat',
        filter=file_filter,
        initialFilter='Excel File (*.xlsx *.xls)'
    )

    return response[0]


def get_file_to_analysis(self: object):
    file_filter = 'Data File (*.xlsx *.csv *.dat);; Excel File (*.xlsx *.xls)'
    response = QFileDialog.getOpenFileName(
        parent=self,
        caption='Select mass specter for analyse',
        directory=os.getcwd(),
        filter=file_filter,
        initialFilter='Excel File (*.xlsx *.xls)'
    )
    return response


def get_directory(self: object):
    response = QFileDialog.getExistingDirectory(
        self,
        caption='Select a folder'
    )
    return response


def ion_alignment(df_to_analyse: pd.DataFrame, matrix_for_alignment: pd.DataFrame):
    molecule = df_to_analyse.loc[:, ~df_to_analyse.columns.isin(
        ["mass", "intensity", "acceptation", "percent"])]
    ion_percent = list()
    df_to_analyse.loc[:, 'code'] = molecule.apply(
        lambda x: "/".join([str(int(x[c])) for c in molecule]), axis=1) if molecule.shape[1] > 1 else molecule.iloc[:, 0]
    for i in range(len(matrix_for_alignment.loc[:, 'code'])):
        transition = df_to_analyse[df_to_analyse.loc[:, 'code']
                                   == matrix_for_alignment.iloc[i, 0]]['percent']
        transition = transition.to_numpy()
        if transition.size == 0:
            transition = 0
        elif transition.size >= 2:
            transition = sum(transition)
        else:
            transition = transition
        ion_percent.append(float(transition))

    return ion_percent


def unitary_statistics(analyse: pd.DataFrame):
    analyse = analyse[analyse.loc[:, 'acceptation'] >= 1]
    analyse.loc[:, "intensity"] = analyse.loc[:,
                                              "intensity"] / analyse.loc[:, "acceptation"]
    intensity_sum = np.sum(analyse.loc[:, "intensity"])
    analyse.loc[:, "percent"] = (
        analyse.loc[:, "intensity"] / intensity_sum)*100

    return analyse


def alignment_matrix(key: pd.DataFrame):
    molecule = key.loc[:, ~key.columns.isin(["mass"])]
    alignment = {}
    alignment["code"] = molecule.apply(lambda x: "/".join([str(int(x[c]))
                                       for c in molecule]), axis=1) if molecule.shape[1] > 1 else molecule.iloc[:, 0]
    alignment["nomenclature"] = molecule.apply(lambda x: "".join([f"[{(x[c])}]{d}" for c, d in zip(
        molecule, molecule.columns.to_list())]), axis=1) if molecule.shape[1] > 1 else molecule.iloc[:, 0]
    alignment["mass"] = key.loc[:, "mass"]

    return pd.DataFrame.from_dict(alignment)


def presentation_settlement(df):
    df["mass"] = df["mass"].round(decimals=1)
    df["%"] = df["percent"].round(decimals=1)
    df.drop(columns=["acceptation", "intensity", "percent"], inplace=True)

    return df


def unitary_ion_filter(df: pd.DataFrame, ion_list: list, key: list):
    buffer = [i for i in ion_list.copy() if i not in key]
    df_to_return = df.copy()
    to_drop = ["nomenclature", "code"]
    if buffer:
        df_to_return["unitary ion"] = np.nan
        to_drop = ["unitary ion"]
        for i in buffer:
            try:
                i = float(i)
                df_to_return.loc[:, 'unitary ion'][(df_to_return.loc[:, "mass"].astype(
                    float)*1.001 > i) & (df_to_return.loc[:, "mass"].astype(float)*0.999 < i)] = "took"
            except ValueError:
                err = QErrorMessage()
                err.showMessage(f"One of your variable is not a float : {i}")
                return err
        df_to_return.dropna(inplace=True)
        df_to_return.drop(columns=to_drop, inplace=True)
        df_to_return.set_index("mass", inplace=True)
    else:
        df_to_return = df_to_return.iloc[0:0]

    return df_to_return


def ion_from_class_filter(df: pd.DataFrame, df_ion: pd.DataFrame, ion_list: list, deepness: str):
    df_inter = df.copy()
    ion_copy = None if isinstance(df_ion, str) else df_ion.copy()
    if ion_list and len(deepness) > 0:
        new_columns = deepness.split("/")
        df_to_return = np.append(df.columns.to_numpy(), new_columns)
        df_shape = df_to_return.shape
        ion_copy = ion_copy[ion_copy.loc[:, new_columns[0]].isin(ion_list)]
        if ion_copy.shape[0] > 0:
            for i in range(ion_copy.shape[0]):
                inter = df_inter[df_inter.loc[:, "code"]
                                 == ion_copy.iloc[i, -1]]
                if inter.shape[0] > 1:
                    inter.reset_index(inplace=True)
                    inter = pd.concat([inter, pd.DataFrame(
                        {l: [ion_copy.iloc[i, k]]*inter.shape[0] for k, l in enumerate(new_columns)})], axis=1).to_numpy()
                elif inter.shape[0] == 1:
                    inter = np.append(
                        inter.to_numpy(), ion_copy.iloc[i, 0:len(new_columns)].to_list())
                if inter.shape == df_shape:
                    df_to_return = np.vstack([df_to_return, inter])
            df_to_return = pd.DataFrame(df_to_return)
            df_to_return.columns = df_to_return.iloc[0, :]
            df_to_return.drop(index=0, inplace=True)
    else:
        df_to_return = df_inter.iloc[0:0]
    return df_to_return


def class_operation(df: pd.DataFrame, type_of_operation: str, deepness: str):
    df_to_return = df.copy()
    deepness = deepness.split("/") if len(deepness) > 0 else None
    if type_of_operation == "No operation":
        df_to_return = check_for_ambiguity(df_to_return, deepness)
        return df_to_return
    else:
        type_of_operation = type_of_operation.replace("sum of ", "")
        if len(type_of_operation) > 0:
            type_of_operation = type_of_operation.split(" ⊂ ")
            df_to_return.loc[:, ~df_to_return.columns.isin(
                ["mass", "code", "nomenclature", *deepness])].astype(float)
            df_to_return = check_for_ambiguity(df_to_return, deepness)
            df_to_return = df_to_return.groupby(by=[*type_of_operation]).sum()
            df_to_return.drop(
                columns=["mass", "code", "nomenclature"], inplace=True)
        return df_to_return


def prepare_df_to_plot(df: pd.DataFrame, type_of_operation: str, deepness: str, mode: str = "default"):
    df_to_return = df.copy()
    if type_of_operation == "No operation" and mode == "default":
        df_to_return.drop(
            columns=['mass', 'nomenclature', 'code', *deepness], inplace=True)
        df_to_return.dropna(axis=1, inplace=True)
        return df_to_return
    elif type_of_operation != "No operation" or mode == "cluster":
        df_to_return.drop(
            columns=['mass', 'nomenclature', 'code'], inplace=True)
        df_to_return.dropna(axis=1, inplace=True)
        return df_to_return


def floatisation(df: pd.DataFrame):
    df_to_return = df.copy().T
    for i in range(len(df_to_return.columns.to_list())):
        try:
            df_to_return.iloc[:, i] = df_to_return.iloc[:, i].astype(float)
        except ValueError:
            pass
    return df_to_return


def check_for_ambiguity(df: pd.DataFrame, deepness: list):
    ambiguous = df.code.to_numpy()
    is_ambiguous = list(
        set([i for i in ambiguous if sum([j == i for j in ambiguous]) > 1]))
    if is_ambiguous:
        for j in is_ambiguous:
            for i in deepness:
                if len(df.loc[:, i][df.loc[:, "code"] == j].unique()) > 1:
                    res = df.loc[:, i][df.loc[:, "code"] == j].unique()
                    values = df.loc[(df.loc[:, 'code'] == j), ~df.columns.isin(
                        ["code", "mass", "nomenclature", *deepness])].iloc[0, :]
                    lower = (df.loc[df.loc[:, i].isin(res), ~df.columns.isin(
                        ["code", "mass", "nomenclature", *deepness])].astype(float).sum()+(1*10**-9)-values*(len(res)))
                    for k in res:
                        upper = (df.loc[(df.loc[:, i] == k) & (df.loc[:, 'code'] != j), ~df.columns.isin(
                            ["code", "mass", "nomenclature", *deepness])].astype(float).sum())
                        m = (upper/lower)*values
                        n = df.loc[(df.loc[:, i] == k) & (df.loc[:, 'code'] == j), df.columns.isin(
                            ["code", "mass", "nomenclature", *deepness])]
                        m, n = m.to_dict(), n.to_dict()
                        m = pd.DataFrame(m | n)
                        df.drop(index=df.loc[(df.loc[:, i] == k) & (
                            df.loc[:, 'code'] == j)].index, inplace=True)
                        df = pd.concat([df, m], axis=0)
                    break
        return df
    else:
        return df


def is_it_float(data: pd.DataFrame, needs: list):
    df = data.copy()
    for i in needs:
        try:
            df.loc[:, i] = df.loc[:, i].astype(float)
        except ValueError:
            pass
    return df
