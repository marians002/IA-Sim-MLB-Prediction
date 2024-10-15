from simulator.postseason import *
from simulator.schedule import *
from metrics.utils import *
from metrics.metrics import compare_metrics


def main():
    teams = dl.load_data()

    schedule = generate_schedule(teams)
    results = save_final_statistics(schedule)

    # Create DataFrames for each division and league
    (nl_east_df, nl_west_df, nl_central_df, nl_overall_df,
     al_east_df, al_west_df, al_central_df, al_overall_df) = create_dataframes_from_results(results, teams)

    (nl_overall_df_original, al_overall_df_original, nl_central_df_original, nl_east_df_original,
     nl_west_df_original, al_central_df_original, al_east_df_original, al_west_df_original) = load_databases()

    # Compare metrics
    n = 5
    compare_metrics(nl_overall_df, al_overall_df, nl_overall_df_original, al_overall_df_original, n, graphics=True)

    al_postseason_teams, nl_postseason_teams = get_postseason_teams(teams)

    # Simulate the postseason
    world_series_winner = create_postseason_structure(nl_postseason_teams, al_postseason_teams)

    print(f"The World Series winner is: {world_series_winner}")


if __name__ == "__main__":
    main()
