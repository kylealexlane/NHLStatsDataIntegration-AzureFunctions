DROP TABLE IF EXISTS nhlstats.yearly_team_against_ranks;

CREATE TABLE nhlstats.yearly_team_against_ranks (
    id                            INT         NOT NULL,
    year_code                     INT         NOT NULL,
    month                         VARCHAR         NOT NULL,
    game_type                     VARCHAR         NOT NULL,


    --Percentile metrics
    num_goals_pctile                      REAL,
    wrist_shot_num_pctile                 REAL,
    backhand_num_pctile                   REAL,
    slap_shot_num_pctile                  REAL,
    snap_shot_num_pctile                  REAL,
    tip_in_num_pctile                     REAL,
    deflected_num_pctile                  REAL,
    wrap_around_num_pctile                REAL,

    wrist_shot_pred_pctile                REAL,
    backhand_pred_pctile                  REAL,
    slap_shot_pred_pctile                 REAL,
    snap_shot_pred_pctile                 REAL,
    tip_in_pred_pctile                    REAL,
    deflected_pred_pctile                 REAL,
    wrap_around_pred_pctile               REAL,

    mean_dist_pctile                      REAL,
    mean_ang_pctile                       REAL,

    sum_xgoals_pctile                     REAL,
    num_shots_pctile                      REAL,
    save_perc_pctile                      REAL,
    shot_quality_pctile                   REAL,

    wrist_shot_freq_pctile                REAL,
    backhand_freq_pctile                  REAL,
    slap_shot_freq_pctile                 REAL,
    snap_shot_freq_pctile                 REAL,
    tip_in_freq_pctile                    REAL,
    deflected_freq_pctile                 REAL,
    wrap_around_freq_pctile               REAL,

    xsave_perc_pctile                     REAL,
    xsave_perc_wrist_shot_pctile          REAL,
    xsave_perc_backhand_pctile            REAL,
    xsave_perc_slap_shot_pctile           REAL,
    xsave_perc_snap_shot_pctile           REAL,
    xsave_perc_tip_in_pctile              REAL,
    xsave_perc_deflected_pctile           REAL,
    xsave_perc_wrap_around_pctile         REAL,

    saves_aa_per_shot_pctile              REAL,

    wrist_shot_save_perc_pctile           REAL,
    backhand_save_perc_pctile             REAL,
    slap_shot_save_perc_pctile            REAL,
    snap_shot_save_perc_pctile            REAL,
    tip_in_save_perc_pctile               REAL,
    deflected_save_perc_pctile            REAL,
    wrap_around_save_perc_pctile          REAL,

    save_perc_aa_pctile                   REAL,

    wrist_shot_freq_aa_pctile             REAL,
    backhand_freq_aa_pctile               REAL,
    slap_shot_freq_aa_pctile              REAL,
    snap_shot_freq_aa_pctile              REAL,
    tip_in_freq_aa_pctile                 REAL,
    deflected_freq_aa_pctile              REAL,
    wrap_around_freq_aa_pctile            REAL,

    xsave_perc_aa_pctile                  REAL,
    xsave_perc_wrist_shot_aa_pctile       REAL,
    xsave_perc_backhand_aa_pctile         REAL,
    xsave_perc_slap_shot_aa_pctile        REAL,
    xsave_perc_snap_shot_aa_pctile        REAL,
    xsave_perc_tip_in_aa_pctile           REAL,
    xsave_perc_deflected_aa_pctile        REAL,
    xsave_perc_wrap_around_aa_pctile      REAL,

    wrist_shot_save_perc_aa_pctile        REAL,
    backhand_save_perc_aa_pctile          REAL,
    slap_shot_save_perc_aa_pctile         REAL,
    snap_shot_save_perc_aa_pctile         REAL,
    tip_in_save_perc_aa_pctile            REAL,
    deflected_save_perc_aa_pctile         REAL,
    wrap_around_save_perc_aa_pctile       REAL,


    --Ranks
    num_goals_rank                     REAL,
    wrist_shot_num_rank                 REAL,
    backhand_num_rank                   REAL,
    slap_shot_num_rank                  REAL,
    snap_shot_num_rank                  REAL,
    tip_in_num_rank                     REAL,
    deflected_num_rank                  REAL,
    wrap_around_num_rank                REAL,

    wrist_shot_pred_rank                REAL,
    backhand_pred_rank                  REAL,
    slap_shot_pred_rank                 REAL,
    snap_shot_pred_rank                 REAL,
    tip_in_pred_rank                    REAL,
    deflected_pred_rank                 REAL,
    wrap_around_pred_rank               REAL,

    mean_dist_rank                      REAL,
    mean_ang_rank                       REAL,

    sum_xgoals_rank                     REAL,
    num_shots_rank                      REAL,
    save_perc_rank                      REAL,
    shot_quality_rank                   REAL,

    wrist_shot_freq_rank                REAL,
    backhand_freq_rank                  REAL,
    slap_shot_freq_rank                 REAL,
    snap_shot_freq_rank                 REAL,
    tip_in_freq_rank                    REAL,
    deflected_freq_rank                 REAL,
    wrap_around_freq_rank               REAL,

    xsave_perc_rank                     REAL,
    xsave_perc_wrist_shot_rank          REAL,
    xsave_perc_backhand_rank            REAL,
    xsave_perc_slap_shot_rank           REAL,
    xsave_perc_snap_shot_rank           REAL,
    xsave_perc_tip_in_rank              REAL,
    xsave_perc_deflected_rank           REAL,
    xsave_perc_wrap_around_rank         REAL,

    saves_aa_per_shot_rank              REAL,

    wrist_shot_save_perc_rank           REAL,
    backhand_save_perc_rank             REAL,
    slap_shot_save_perc_rank            REAL,
    snap_shot_save_perc_rank            REAL,
    tip_in_save_perc_rank               REAL,
    deflected_save_perc_rank            REAL,
    wrap_around_save_perc_rank          REAL,

    save_perc_aa_rank                   REAL,

    wrist_shot_freq_aa_rank             REAL,
    backhand_freq_aa_rank               REAL,
    slap_shot_freq_aa_rank              REAL,
    snap_shot_freq_aa_rank              REAL,
    tip_in_freq_aa_rank                 REAL,
    deflected_freq_aa_rank              REAL,
    wrap_around_freq_aa_rank            REAL,

    xsave_perc_aa_rank                  REAL,
    xsave_perc_wrist_shot_aa_rank       REAL,
    xsave_perc_backhand_aa_rank         REAL,
    xsave_perc_slap_shot_aa_rank        REAL,
    xsave_perc_snap_shot_aa_rank        REAL,
    xsave_perc_tip_in_aa_rank           REAL,
    xsave_perc_deflected_aa_rank        REAL,
    xsave_perc_wrap_around_aa_rank      REAL,

    wrist_shot_save_perc_aa_rank        REAL,
    backhand_save_perc_aa_rank          REAL,
    slap_shot_save_perc_aa_rank         REAL,
    snap_shot_save_perc_aa_rank         REAL,
    tip_in_save_perc_aa_rank            REAL,
    deflected_save_perc_aa_rank         REAL,
    wrap_around_save_perc_aa_rank       REAL,

    created                       TIMESTAMP DEFAULT current_timestamp,
    PRIMARY KEY(id, year_code, month, game_type)
);
