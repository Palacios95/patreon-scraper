import pandas as pd
import numpy as np
import re

patron_df = pd.read_json(r"patreon_data/output.json")

print(patron_df.reward_tiers)

patron_df.reward_tiers = patron_df.reward_tiers.apply(
    lambda x: list(map(lambda y: re.sub("[^0-9.]", "", y), x))
)

# grab number of users without a creator_id
no_cid = len(patron_df.loc[patron_df["creator_id"].str.contains("user?")].index)
# grab number of rows without any patorns
no_patrons = len(patron_df.loc[patron_df["patron_count"] == "0"].index) + len(
    patron_df.loc[patron_df["patron_count"].isnull()]
)
# grab number of rows with no income
no_income = len(patron_df.loc[patron_df["monthly_income"] == "$0"].index)
# + \ len(patron_df.loc[patron_df['monthly_income'].isnull()]) ##TODO: Set this equal to avg_reward * num of patrons

# clean df

patron_df = patron_df.loc[~patron_df["creator_id"].str.contains("user?")]
patron_df = patron_df.loc[patron_df["patron_count"] != "0"]
patron_df = patron_df.loc[~patron_df["patron_count"].isnull()]
patron_df = patron_df.loc[patron_df["monthly_income"] != "$0"]
patron_df = patron_df.reset_index(drop=True)

# remove $ character from reward_tiers TODO: clean reward tiers so that all entries are integers
values = []
for row in patron_df["reward_tiers"]:
    try:
        values.append(row[0])
    except IndexError:
        pass
print("unique values for reward_tiers:")
print(set(values))

# calc avg_reward TODO: Calc average reward as new column, currently 0
patron_df["avg_reward"] = np.mean([0])

# calc adj_monthly_income- TODO: Replace Monthly Income with num_patrons * avg revward tier
patron_df["adj_monthly_income"] = patron_df["monthly_income"]

with pd.option_context("display.max_rows", 10, "display.max_columns", None):
    print(patron_df)
print("rows with no patrons", no_patrons)
print("rows with no creator id", no_cid)
print("rows with no monthly income", no_income)

