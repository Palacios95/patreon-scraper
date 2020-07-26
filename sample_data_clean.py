import pandas as pd
import numpy as np
import re

patron_df = pd.read_json(r"patreon_data/output.json")

patron_df.reward_tiers = patron_df.reward_tiers.apply(
    lambda x: list(map(lambda y: y.replace(",", ""), x))
)

# Ensure only creators with dollar amount reward tiers are in dataset
non_dollar_reward_tier_row_ids = []
for index, row in patron_df.iterrows():
    for reward_tier in row["reward_tiers"]:
        if not re.match(
            "^[$]?[+-]?[0-9]{1,3}(?:,?[0-9]{3})*(?:\.[0-9]{2})?$", reward_tier
        ):
            non_dollar_reward_tier_row_ids.append(index)
            break

patron_df.drop(patron_df.index[non_dollar_reward_tier_row_ids], inplace=True)

# Remove dollar signs from reward tiers
patron_df.reward_tiers = patron_df.reward_tiers.apply(
    lambda x: list(map(lambda y: y.replace("$", ""), x))
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


# calc avg_reward TODO: Calc average reward as new column, currently 0
bad_row_indicies = []
for index, row in patron_df.iterrows():
    for x in row["reward_tiers"]:
        try:
            x = float(x)
        except ValueError:
            bad_row_indicies.append(row.name)

# Show number of rows before drop
print("# of rows before drop \n", len(patron_df))
final_df = patron_df.drop(patron_df.index[bad_row_indicies])
final_df = final_df.reset_index(drop=True)
print("# of rows in final df \n", len(final_df))

final_df["reward_tiers"] = final_df["reward_tiers"].apply(lambda x: list(map(float, x)))
final_df["average_reward"] = final_df["reward_tiers"].apply(
    lambda x: round(np.mean(x), 2)
)

# calc adj_monthly_income- TODO: Replace Monthly Income with num_patrons *
# avg reward tier
final_df["patron_count"] = final_df["patron_count"].apply(
    lambda x: float(x.replace(",", ""))
)
# print(type(final_df["patron_count"][0]))
final_df = final_df.loc[final_df['average_reward'].isnull()==False]
final_df.reset_index(drop=True, inplace=True)
final_df["adj_monthly_income"] = final_df["patron_count"] * final_df['average_reward']

with pd.option_context("display.max_rows", 10, "display.max_columns", None):
    print(final_df)
print("rows with no patrons", no_patrons)
print("rows with no creator id", no_cid)
print("rows with no monthly income", no_income)
