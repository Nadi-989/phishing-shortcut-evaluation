# Data

The datasets are not stored in this repository. Both are public.

## PhiUSIIL Phishing URL Dataset

* Source: UCI Machine Learning Repository, dataset 967
  https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset
* 235,795 URLs (134,850 legitimate, 100,945 phishing), 54 features plus label.
* The notebook downloads it automatically with `ucimlrepo` (`fetch_ucirepo(id=967)`).
* Original label: 1 = legitimate, 0 = phishing. The notebook inverts it so that phishing = 1.

## WPD, Web page phishing detection

* Source: Mendeley Data, A. Hannousse and S. Yahiouche, version 3, doi:10.17632/c2gw7fy2j4.3
  https://data.mendeley.com/datasets/c2gw7fy2j4/3
* 11,430 URLs (balanced), 87 features plus the raw URL and the `status` label.
* Download the archive, take `dataset_B_05_2020.csv`, and rename it to `dataset_phishing.csv`.
  Place it next to the notebook (or upload it to the Colab file panel).
