import pyproj
import pandas
import geopandas
import xUtility
import Importers
import DividedHighways
import xLTS
from typing import List, Dict
from Nodes import Node_
from Segments import Segment_, Junction_, JuncLeg_
import GeoJuncs
import Legs
import Crossing
from MovementRelationData import MovementRelation_

geod = pyproj.Geod(ellps='WGS84')


class Geoatoms(
    xUtility.Mixin,
    Importers.Mixin,
    DividedHighways.Mixin,
    xLTS.Mixin,
    GeoJuncs.GeoJuncs,
    Legs.Mixin,
    Crossing.Mixin

):
    def __init__(self):
        self._in_node_id: int = 100
        self._in_seg_id: int = 100
        self._in_rel_id: int = 100
        self._buffersize: float = 0.0002
        self.nodes_reversed_dict: Dict[str, Node_] = {}
        self.nodeid_to_reversedicindex: Dict[int, str] = {}
        self.segments_dict: Dict[int, Segment_] = {}
        self.juncs_dict: Dict[int, Junction_] = {}
        self.legs_dict: Dict[int, JuncLeg_] = {}
        self.field_val_spec_dual_cargwy = Dict[str, str]
        self.field_street_name = str
        self.field_id = str
        self.crossing_dict: Dict[int, MovementRelation_] = {}

    def get_or_add_node_id(self, latlng: tuple) -> int:
        """
        strategy for making the reversed dictrionary depends on the data input
        :param latlng: coordinates
        :return: id of the node
        """
        try:
            _n = self.nodes_reversed_dict[f"{float(latlng[0]):.15f}{float(latlng[1]):.15f}"]
            return _n.id

        except KeyError:
            _id = self._in_node_id
            _n = Node_(id=_id, lon=latlng[0], lat=latlng[1])
            self.nodes_reversed_dict.update({
                f"{float(latlng[0]):.15f}{float(latlng[1]):.15f}": _n
            })
            self._in_node_id = _id + 1
            return _n.id

    def crossing_movements(self
                           ) -> geopandas.GeoDataFrame:

        for node_d in self.nodes_reversed_dict:
            # intersections
            if len(self.nodes_reversed_dict[f"{node_d}"].incident_segments) > 2:
                node_id = self.nodes_reversed_dict[f"{node_d}"].id
                if len(self.nodes_reversed_dict[f"{node_d}"].dual_name_to_nodeid) == 0:
                    is_on_dual_cargway = False
                    for incid_seg_id_ in self.nodes_reversed_dict[f"{node_d}"].incident_segments:
                        is_on_dual_cargwy_val = self.get_segment_attributes(incid_seg_id_, [
                            list(self.field_val_spec_dual_cargwy.keys())[0]])
                        if is_on_dual_cargwy_val[0] == self.field_val_spec_dual_cargwy[
                            list(self.field_val_spec_dual_cargwy.keys())[0]]:
                            is_on_dual_cargway = True

                if is_on_dual_cargway:  # SHOULD THIS BE IF ^^
                    # TODO THIS NEED TO BE CHECKED - I THINK IT WILL BE FINE BUT...
                    for incid_seg_id_ in self.nodes_reversed_dict[f"{node_d}"].incident_segments:
                        street_names = self.get_segment_attributes(incid_seg_id_, [self.field_street_name])
                        is_on_dual_cargwy_val = self.get_segment_attributes(incid_seg_id_, [
                            list(self.field_val_spec_dual_cargwy.keys())[0]])
                        if (
                                (
                                        is_on_dual_cargwy_val[0] == self.field_val_spec_dual_cargwy[list(
                                    self.field_val_spec_dual_cargwy.keys()
                                )[0]]
                                ) and
                                (
                                        street_names[0] not in ['NULL', None, '', 'None']
                                )
                        ):
                            pair_node_id = self.node_winc_segm_wsam_name(tname=street_names[0], this_node_d=node_d)
                            if len(pair_node_id) > 0:
                                self.nodes_reversed_dict[
                                    f"{self.nodeid_to_reversedicindex[node_id]}"].dual_name_to_nodeid.update({
                                    f'{street_names[0]}': pair_node_id[0]
                                })
                else:
                    incid_seg_ids_ = []
                    bearings = []
                    incident_seg_geoms = []
                    inc_seg_index_control = 0
                    while len(self.nodes_reversed_dict[f"{node_d}"].incident_segments) < inc_seg_index_control:
                        incident_seg_geom = self.inc_seg_geom(incid_seg_id_, node_id)
                        if len(incident_seg_geom) == 0:
                            continue
                        bearing = self.get_bearing(incident_seg_geom[0], incident_seg_geom[1])
                        incid_seg_ids_.append(incid_seg_id_)
                        bearings.append(bearing)
                        incident_seg_geoms.append(incident_seg_geom)
                        inc_seg_index_control += 1
                    # for incid_seg_id_ in self.nodes_reversed_dict[f"{node_d}"].incident_segments:
                    #     incident_seg_geom = self.inc_seg_geom(incid_seg_id_, node_id)
                    #
                    #     bearing = self.get_bearing(incident_seg_geom[0], incident_seg_geom[1])
                    #     incid_seg_ids_.append(incid_seg_id_)
                    #     bearings.append(bearing)
                    #     incident_seg_geoms.append(incident_seg_geom)

                    incident_segs_df = pandas.DataFrame(
                        {
                            'incid_seg_id_': incid_seg_ids_,
                            'bearing': bearings,
                            'adj_inc_seg_geom': incident_seg_geoms
                        }
                    )
                    incident_segs_df['cc_rank'] = incident_segs_df['bearing'].rank(ascending=False, method='first')
                    self.nodes_reversed_dict[f"{node_d}"].cc_ordered_incident_segments.append(incident_segs_df)
                    #     hopefully this will end up exactly same way for multi node intersections but for now
                    #     until the med point process is implemented
                    #     this checks to run for only simple node intersections'
                    # for i_ in range(len(incident_segs_df)):
                    #     for j_ in range(len(incident_segs_df)):
                    #         if i_ != j_:
                    #             # if j_ == i_ + 2:
                    #             gdf, row_indx = self.do_all_movements(
                    #                 node_d,
                    #                 incident_segs_df,
                    #                 i_,
                    #                 j_,
                    #                 from_attributes_wanted,
                    #                 to_attributes_wanted,
                    #                 crossed_over_attributes_wanted,
                    #                 gdf,
                    #                 row_indx,
                    #                 is_multi=False
                    #             )
                    # need make sure to save these to update the self.nodeid_to_reversedicindex after the iteration

        # new_merged_ids, new_meged_verts = self.one_dual_carriage_way()
        # # print(new_merged_ids, new_meged_verts)
        # for _m_i_ in range(len(new_merged_ids)):
        #     new_merged_id_ = new_merged_ids[_m_i_]
        #     vert = new_meged_verts[_m_i_]
        #     self.nodeid_to_reversedicindex.update({
        #         new_merged_id_: f"{float(vert[0]):.15f}{float(vert[1]):.15f}"
        #     })
        # new_merged_ids2, new_meged_verts2 = self.two_dual_carriage_way()
        # for _m_i_2 in range(len(new_merged_ids2)):
        #     new_merged_id_2 = new_merged_ids2[_m_i_2]
        #     vert2 = new_meged_verts2[_m_i_2]
        #     self.nodeid_to_reversedicindex.update({
        #         new_merged_id_2: f"{float(vert2[0]):.15f}{float(vert2[1]):.15f}"
        #     })
        # TODO: check if you need to remove this part to the end
        # for mmnode_id in self.nodeid_to_reversedicindex:
        #     if len(
        #             self.nodes_reversed_dict[f"{self.nodeid_to_reversedicindex[mmnode_id]}"].incident_segments
        #     ) > 2:
        #         # if len(
        #         #         self.nodes_reversed_dict[f"{self.nodeid_to_reversedicindex[mmnode_id]}"].is_multinode_processed
        #         # ) > 0:
        #         mincid_seg_ids_ = []
        #         mbearings = []
        #         mincident_seg_geoms = []
        #         for mincid_seg_id_ in self.nodes_reversed_dict[
        #             f"{self.nodeid_to_reversedicindex[mmnode_id]}"
        #         ].incident_segments:
        #             mincident_seg_geom = self.inc_seg_geo_for_multinodes(mincid_seg_id_, mmnode_id)
        #             if len(mincident_seg_geom) > 0:
        #                 mbearing = self.get_bearing(mincident_seg_geom[0], mincident_seg_geom[1])
        #                 mincid_seg_ids_.append(mincid_seg_id_)
        #                 mbearings.append(mbearing)
        #                 mincident_seg_geoms.append(mincident_seg_geom)
        #         mincident_segs_df = pandas.DataFrame(
        #             {
        #                 'incid_seg_id_': mincid_seg_ids_,
        #                 'bearing': mbearings,
        #                 'adj_inc_seg_geom': mincident_seg_geoms
        #             }
        #         )
        #         mincident_segs_df['cc_rank'] = mincident_segs_df['bearing'].rank(ascending=False, method='first')
        #         self.nodes_reversed_dict[
        #             f"{self.nodeid_to_reversedicindex[mmnode_id]}"
        #         ].cc_ordered_incident_segments.append(mincident_segs_df)
        #         #     hopefully this will end up exactly same way for multi node
        #         #     intersections but for now until the med point process is
        #         #     implemented this checks to run for only simple node intersections'
        #         for mi_ in range(len(mincident_segs_df)):
        #             for mj_ in range(len(mincident_segs_df)):
        #                 if mi_ != mj_:
        #                     gdf, row_indx = self.do_all_movements(
        #                         self.nodeid_to_reversedicindex[mmnode_id],
        #                         mincident_segs_df,
        #                         mi_,
        #                         mj_,
        #                         from_attributes_wanted,
        #                         to_attributes_wanted,
        #                         crossed_over_attributes_wanted,
        #                         gdf,
        #                         row_indx,
        #                         is_multi=True
        #                     )
        #
        # gdf.crs = pyproj.CRS.from_epsg(4326).to_wkt()
        # self.gdfs.append(gdf)
        # return gdf
