from __future__ import annotations

import streamlit as st

import genetic_forensic_portal.app.utils.familial_analysis_utils as fam_utils
from genetic_forensic_portal.app.client import gf_api_client as client
from genetic_forensic_portal.app.client import keycloak_client as auth_client
from genetic_forensic_portal.app.common import download_buttons, setup
from genetic_forensic_portal.app.common.constants import AUTHENTICATED, ROLES, USERNAME

st.title("Comprehensive Analysis Overview")

setup.initialize()

if st.session_state[AUTHENTICATED]:
    # Get the first page of analyses (UUIDs)
    response = client.list_analyses()
    uuid_list = response.analyses

    # Ensure uuid_list is iterable and can be passed to selectbox
    uuid = st.selectbox(
        "Select a sample ID",
        uuid_list,
        index=None,
        placeholder="Select sample ID...",
    )

    if uuid:
        analysis_results = client.get_all_analyses(uuid)

        # Create columns for the layout
        col1, col2 = st.columns(2)

        # Display SCAT analysis in the first column
        if analysis_results.scat:
            col1.image(analysis_results.scat, caption="SCAT Analysis")
        else:
            col1.error("SCAT Analysis not found")

        # Display Voronoi analysis in the second column
        if analysis_results.voronoi:
            col2.image(analysis_results.voronoi, caption="Voronoi Analysis")
        else:
            col2.error("Voronoi Analysis not found")

        # Display the Familial analysis below
        if (
            analysis_results.familial is not None
            and not analysis_results.familial.empty
        ):
            st.write("Familial Analysis")
            st.dataframe(
                analysis_results.familial.style.map(
                    fam_utils.highlight_exact_matches,
                    subset=[fam_utils.EXACT_MATCH_COLUMN],
                )
            )
        else:
            st.error("Familial Analysis not found")

        if auth_client.check_download_access(
            st.session_state[USERNAME], st.session_state[ROLES], uuid
        ):
            download_buttons.scat_analysis_download_button(uuid)
            download_buttons.voronoi_analysis_download_button(uuid)
