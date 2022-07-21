import os
import pandas as pd
import matplotlib.pyplot as plt


subfolders = [ f.path for f in os.scandir(".") if f.is_dir() ]


for path in subfolders:
    path = path.split("./")[1]
    if not path.startswith("apo"):
        continue

    filenames = os.listdir(path)
    csvs = [ filename for filename in filenames if filename.endswith( ".CSV" ) or filename.endswith( ".csv" )]
    csvs.sort()

    result = {
        "320": [],
        "440": []
    } 

    for csv in csvs:
        df = pd.read_csv(path + "/" + csv, encoding="utf-16le")
        wv320 = df.loc[df['Wavelength (nm)'] == 320]["Absorbance (AU)"].values[0]
        wv440 = df.loc[df['Wavelength (nm)'] == 440]["Absorbance (AU)"].values[0]
        wv800 = df.loc[df['Wavelength (nm)'] == 800]["Absorbance (AU)"].values[0]

        result["320"].append(wv320 - wv800)
        result["440"].append(wv440 - wv800)

    out_df = pd.DataFrame(result, columns=result.keys())
    out_df.to_csv("./output/" + path + ".csv")


    x = [i for i in range(len(result["320"]))]

    plt.plot(x, result["320"], label=(path + " - 320 - 800"), marker="o")
    plt.plot(x, result["440"], label=(path + " - 440 - 800"), marker="o")
    plt.legend(loc="upper right")

plt.show()
