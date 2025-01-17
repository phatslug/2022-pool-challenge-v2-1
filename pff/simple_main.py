import pandas as pd
import numpy as np
from pathlib import Path
import json

pos_cols = [f"{ax}_position" for ax in ["x", "y", "z"]]
res_cols = ["msec", "subject", "trial"]


if __name__ == "__main__":
    df = pd.read_pickle("data.pkl")
    input_locations = json.loads(Path("input.json").read_text())
    numpy_df = df.loc[:, pos_cols + res_cols].to_numpy()
    numpy_input = pd.DataFrame(input_locations).to_numpy()

    def solution_list(numpy_df, numpy_input):
        out = []
        for i in range(len(numpy_input)):
            mask = (
                (numpy_df[:, [-3]] >= numpy_input[:, [-2]][i][0])
                & (numpy_df[:, [-3]] <= numpy_input[:, [-1]][i][0])
                & (numpy_df[:, [-2]] == numpy_input[:, [-3]][i][0])
            )
            pos_arr = np.array([numpy_input[0][c] for c in [0, 1, 2]], ndmin=2)
            dumma = (
                (numpy_df[:, [0]][mask] - numpy_input[:, [0]][i]) ** 2
                + (numpy_df[:, [1]][mask] - numpy_input[:, [1]][i]) ** 2
                + (numpy_df[:, [2]][mask] - numpy_input[:, [2]][i]) ** 2
            )
            msec = numpy_df[:, [-3]][mask][np.where(dumma == np.amin(dumma))[0][0]]
            subject = numpy_df[:, [-2]][mask][np.where(dumma == np.amin(dumma))[0][0]]
            trial = numpy_df[:, [-1]][mask][np.where(dumma == np.amin(dumma))[0][0]]
            out.append({"msec": msec, "subject": subject, "trial": trial})
        return out

    Path("output.json").write_text(json.dumps(solution_list(numpy_df, numpy_input)))
