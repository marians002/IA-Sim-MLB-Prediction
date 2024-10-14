from simulator.postseason import *
from simulator.schedule import *
from metrics.utils import *


def main():
    teams = dl.load_data()

    schedule = generate_schedule(teams)
    results = save_final_statistics(schedule)

    # Create DataFrames for each division and league
    # (nl_east_df, nl_west_df, nl_central_df, nl_overall_df,
     # al_east_df, al_west_df, al_central_df, al_overall_df) = create_dataframes_from_results(results)

    # # Print the American League DataFrames
    # print("AL East DataFrame:")
    # print(al_east_df)
    # print("\nAL Central DataFrame:")
    # print(al_central_df)
    # print("\nAL West DataFrame:")
    # print(al_west_df)
    # print("\nAL Overall DataFrame:")
    # print(al_overall_df)

    # # Load the original CSV data
    # nl_overall_df_original = pd.read_csv('NL_OVERALL.CSV')
    # nl_central_df_original = pd.read_csv('NL_CENTRAL_DIVISION.CSV')
    # nl_east_df_original = pd.read_csv('NL_EAST_DIVISION.CSV')
    # nl_west_df_original = pd.read_csv('NL_WEST_DIVISION.CSV')
    # al_overall_df_original = pd.read_csv('AL_OVERALL.CSV')
    # al_central_df_original = pd.read_csv('AL_CENTRAL_DIVISION.CSV')
    # al_east_df_original = pd.read_csv('AL_EAST_DIVISION.CSV')
    # al_west_df_original = pd.read_csv('AL_WEST_DIVISION.CSV')

    al_postseason_teams, nl_postseason_teams = get_postseason_teams(teams)

    # Simulate the postseason
    world_series_winner = create_postseason_structure(nl_postseason_teams, al_postseason_teams)

    print(f"The World Series winner is: {world_series_winner}")


if __name__ == "__main__":
    main()
