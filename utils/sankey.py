import pandas as pd
import numpy as np
# from majors.database_handler import DatabaseHandler
import plotly.graph_objects as go
# import matplotlib.pyplot as plt
from utils.color_utils import lighten_color

class SankeyDiagram:
    @staticmethod
    def process_data(df, selected_columns, drop:str):
        drop = drop
        def groupby_df(selected_columns, df):
            dfs = [] 
            for i in range(len(selected_columns) - 1):
                grouped_df = df.groupby([selected_columns[i], selected_columns[i + 1]])['student_id'].count().reset_index()
                grouped_df.columns = ['source', 'target', 'value']
                dfs.append(grouped_df)

            overall_df = pd.concat(dfs, axis=0)
            final_df = dfs[-1]  
            return overall_df, final_df

        def set_drop_value(df, drop):
            if 'value' in df.columns:
                df.loc[
                    df['source'].str.contains(drop, case=False, na=False), 'value'] = 0
            return df

        grouped_df, final_df = groupby_df(selected_columns, df)
        grouped_df = set_drop_value(grouped_df, drop)
        final_df = set_drop_value(final_df, drop)
        return grouped_df, final_df

    @staticmethod
    def find_unique_mapping(df1, df2):
        unique_source_target = list(pd.unique(df1[['source', 'target']].values.ravel('K')))
        mapping_dict = {value: idx for idx, value in enumerate(unique_source_target)}

        df1['source'] = df1['source'].map(mapping_dict)
        df1['target'] = df1['target'].map(mapping_dict)
        df2['source'] = df2['source'].map(mapping_dict)
        df2['target'] = df2['target'].map(mapping_dict)

        df_dict = df1.to_dict(orient='list')
        final_dict = df2.to_dict(orient='list')

        return unique_source_target, df_dict, final_dict, mapping_dict

    @staticmethod
    def calculate_total_values_by_source(df_dict, mapping_dict):
        df_tempt = pd.DataFrame(df_dict)

        drop_values = [value for key, value in mapping_dict.items() if 'NGHI_HOC' in key or 'NGHỈ HỌC' in key]

        specific_rows = df_tempt[df_tempt['target'].isin(drop_values)]

        total_values_by_source = df_tempt[~df_tempt['source'].isin(drop_values)].groupby('source')['value'].sum()

        if not specific_rows.empty:
            total_values_by_target_for_specific = specific_rows.groupby('target')['value'].sum()
            total_values_by_source = pd.concat([total_values_by_source, total_values_by_target_for_specific]).to_dict()

        return total_values_by_source

    @staticmethod
    def calculate_total_values_by_target(final_df):
        df = pd.DataFrame(final_df)
        total_values_by_target = df.groupby('target')['value'].sum().to_dict()
        return total_values_by_target

    @staticmethod
    def draw_sankey(df_dict, final_dict, unique_source_target, color_list, mapping_dict, heigth=350, width=1200):
        total_values_by_source = SankeyDiagram.calculate_total_values_by_source(df_dict, mapping_dict)
        total_values_by_target =SankeyDiagram.calculate_total_values_by_target(final_dict)
        labeled_nodes = []

        for i, label in enumerate(unique_source_target):
            source_value = total_values_by_source.get(i)
            target_value = total_values_by_target.get(i)

            if source_value is not None:
                labeled_nodes.append(f"{label}: {source_value}")
            else:
                labeled_nodes.append(f"{label}: {target_value}")

        link_colors = [lighten_color(color_list[src % len(color_list)]) for src in df_dict['source']]

        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labeled_nodes, 
                color=color_list[:len(unique_source_target)]  
            ),
            textfont=dict(
                color='black',
                size=10,
                family="Tahoma"
            ),
            link=dict(
                source=df_dict['source'],
                target=df_dict['target'],
                value=df_dict['value'],
                color=link_colors
            ))])

        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',  
            margin=dict(
                l=50,  
                r=50,  
                t=20,  
                b=20   
            ),
            height=heigth,
            width=width
        )

        return fig
    


