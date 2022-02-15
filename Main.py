import geopandas
import GeoAtoms

geopandas.options.display_precision = 9
# TODO: CHANGE TO geobase_dual_4326.gpkg
streets = geopandas.read_file('C:\\Users\\bitas\\folders\\Research\\Montreal\\codes\\intersection\\Nov1\\'
                              'geobase_dual_4326.gpkg')
print("streets:", len(streets))
#
#
# osm_traffic_signals = geopandas.read_file('osm.traffic.signals_s2.gpkg')
# traffic_signals = geopandas.read_file('traffic.signals_s2.gpkg')
# signs = geopandas.read_file('signs_s2.gpkg')
# channelized_right_turns =  geopandas.read_file('channelized_right_turns.gpkg')
# intersection_treatments =  geopandas.read_file('intersection_treatments_s2.gpkg')


from_attributes_wanted = [
    # 'ID_TRC',
    'CLASSE',
    'SENS_CIR', 'ONEWAY',
    'POSITION_R', 'NOM_VOIE'
]

to_attributes_wanted = [
    # 'ID_TRC',
    'CLASSE',
    'SENS_CIR', 'ONEWAY',
    'POSITION_R', 'NOM_VOIE'

]

crossed_over_attributes_wanted = [
    # 'ID_TRC',
    'ONEWAY',
    'SENS_CIR',
    'NOM_VOIE'
    # 'ID_CYCL'
    # 'NetworkiD', 'LANE_THRU',
    # 'R_LANE_W', 'R_LTL_W',
    # 'LT_LTL_W', 'R_SHLDR_W',
    # 'L_SHLDR_W', 'R_BL_W',
    # 'L_BL_W',
    # 'SPEEDLIMIT', 'FL33T85',
    # 'ONEWAY', 'CURRENT_AA',
    # 'ROAD', 'v4_FID'

]
trc_attributes_wanted = [
    'ID_TRC'
]
streets = streets[streets['geometry'].is_valid]
#
# stop_signs = signs.loc[signs['MUTCD'].isin([
#     'R1-9','R2-1', 'R1-6A', 'R1-6', 'R1-5C',
#     'R1-5A', 'R1-5', 'R1-3P', 'R1-2', 'R1-1',
#     'R10-6', 'R10-4A', 'R10-4', 'R10-3E-DE3',
#     'R10-3B'])]
#
# stop_signs.set_crs(epsg=4326, inplace=True)
# stop_signs = stop_signs[stop_signs['geometry'].is_valid]
#
# osm_traffic_signals.set_crs(epsg=4326, inplace=True)
# osm_traffic_signals = osm_traffic_signals[osm_traffic_signals['geometry'].is_valid]
#
# traffic_signals.set_crs(epsg=4326, inplace=True)
# traffic_signals = traffic_signals[traffic_signals['geometry'].is_valid]
#
# channelized_right_turns.set_crs(epsg=4326, inplace=True)
# channelized_right_turns = channelized_right_turns[channelized_right_turns['geometry'].is_valid]
#
# intersection_treatments.set_crs(epsg=4326, inplace=True)
# intersection_treatments = intersection_treatments[intersection_treatments['geometry'].is_valid]
#
#
# rrfbs = intersection_treatments.loc[intersection_treatments['RRFB'] == 1, ]
# xislands = intersection_treatments.loc[intersection_treatments['XING_ISLND'] == 1, ]


ga = GeoAtoms.Geoatoms()

ga.first_order_import(streets, field_val_spec_dual_cargwy={'ONEWAY': 'DIVIDED'}, field_street_name='NOM_VOIE')

#
# ga.second_order_import([
# {
#         'geodataframe': traffic_signals,
#         'name': 'traffic_signals',
#         'field_to_fetch': 'TYPE'
#     },
#     {
#         'geodataframe': osm_traffic_signals,
#         'name': 'osm_traffic_signals',
#         'field_to_fetch': 'highway'
#     },
#     {
#         'geodataframe': stop_signs,
#         'name': 'stop_signs',
#         'field_to_fetch': 'RDWAY_ID'
#     },
#     {
#         'geodataframe': rrfbs,
#         'name': 'rrfbs',
#         'field_to_fetch': 'RRFB'
#     },
#     {
#         'geodataframe': xislands,
#         'name': 'xislands',
#         'field_to_fetch': 'XING_ISLND'
#     },
#     {
#         'geodataframe': channelized_right_turns,
#         'name': 'channelized_right_turns',
#         'field_to_fetch': 'fclass_tra'
#     }
#
# ])

# some kind of set up that could be used to tell the geoatoms  what attributes are
# fetch from to, from, and crossed over segments and saved with the geometry


ga.crossing_movements()
# this is where we only doing the through crossing part is happeingn s
# so one idea is to preemptively count for that and store the information in a list
#                         incident


gdf_junc = ga.junc_layer(my_id='ID_TRC')
ga.legLookUp()
gdf = ga.do_simple_crossing(from_attributes_wanted=from_attributes_wanted,
                            to_attributes_wanted=to_attributes_wanted,
                            crossed_over_attributes_wanted=crossed_over_attributes_wanted,
                            trc_attributes_wanted=trc_attributes_wanted)


gdf.to_file(
    'crossing_1.gpkg',
    layer='crossing_101',
    driver="GPKG"
)

# gdf_junc.to_file(
#     'junc_layer.gpkg',
#     layer='junc_layer_1',
#     driver="GPKG"
# )

# gdf_junc.to_csv('juncLayer1.csv')
# there is no point in saving the crossing if either the from or to segments lts is 4 since the crossing lts can't be
# worse than that

# gdf_exp = gdf.loc[
#     (gdf['t_LTS_MAX'] != 4) &
#     (gdf['f_LTS_MAX'] != 4)
#     # (gdf['c_ONEWAY'] == 'Divided') &
#     # (gdf['f_ONEWAY'] != 'Divided') &
#     # (gdf['t_ONEWAY'] != 'Divided')
# ]
# gdf.to_file(
#     'crossing_relations_m_3.gpkg',
#     layer='crossing_relations_m_513',
#     driver="GPKG"
# )
