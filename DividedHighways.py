import collections
class Mixin:
    # def one_dual_carriage_way(self):  # TODO: CHECK IF NEED TO REMOVE
    #     new_merged_ids = []
    #     new_meged_verts = []
    #     for node_id in self.nodeid_to_reversedicindex:
    #         if len(self.nodes_reversed_dict[f'{self.nodeid_to_reversedicindex[node_id]}'].incident_segments) > 2:
    #             # node_id = self.nodes_reversed_dict[f"{node_d}"].id
    #
    #             if len(self.nodes_reversed_dict[f'{self.nodeid_to_reversedicindex[node_id]}'].dual_name_to_nodeid) > 0:
    #                 # print('merging for each street namer')
    #                 for stname in self.nodes_reversed_dict[
    #                     f'{self.nodeid_to_reversedicindex[node_id]}'
    #                 ].dual_name_to_nodeid:
    #                     _nid_to_merge = self.nodes_reversed_dict[
    #                         f'{self.nodeid_to_reversedicindex[node_id]}'
    #                     ].dual_name_to_nodeid[stname]
    #
    #                     new_merged_id, loc_prps = self.merge_two_nodes(node_id, _nid_to_merge)
    #                     new_merged_ids.append(new_merged_id)
    #                     new_meged_verts.append(loc_prps)
    #     return new_merged_ids, new_meged_verts

    # def two_dual_carriage_way(self):  # TODO: REMOVE IF NOT USED
    #     # new_merged_ids = []
    #     # new_meged_verts = []
    #
    #     for node_id in self.nodeid_to_reversedicindex:
    #         if len(self.nodes_reversed_dict[f'{self.nodeid_to_reversedicindex[node_id]}'].incident_segments) > 2:
    #             # node_id = self.nodes_reversed_dict[f"{node_d}"].id
    #
    #             if len(self.nodes_reversed_dict[f'{self.nodeid_to_reversedicindex[node_id]}'].dual_name_to_nodeid) > 0:
    #                 family_nodes = [node_id]
    #                 # print('merging for each street namer')
    #                 for stname in self.nodes_reversed_dict[
    #                     f'{self.nodeid_to_reversedicindex[node_id]}'
    #                 ].dual_name_to_nodeid:
    #                     _nid_to_merge = self.nodes_reversed_dict[
    #                         f'{self.nodeid_to_reversedicindex[node_id]}'
    #                     ].dual_name_to_nodeid[stname]
    #                     family_nodes.append(_nid_to_merge)
    #
    #                     # new_merged_id, loc_prps = self.merge_two_nodes(node_id, _nid_to_merge)
    #                     # # print(new_merged_id, loc_prps)
    #                     # new_merged_ids.append(new_merged_id)
    #                     # new_meged_verts.append(loc_prps)
    #     # return new_merged_ids, new_meged_verts
    #     return family_nodes

    def merge_nodes(self, nodes_id_lst: list):
        # family_nodes = []
        lats = []
        lons = []
        combin_inc_segs = []

        for _node_id in nodes_id_lst:
            node_ = self.nodes_reversed_dict[f'{self.nodeid_to_reversedicindex[_node_id]}']
            lats.append(node_.lat)
            lons.append(node_.lon)
            combin_inc_segs.append(node_.incident_segments)

        m_lon = sum(lons) / len(lons)
        m_lat = sum(lats) / len(lats)

        loc_prps = [m_lon, m_lat]
        m_node_id = self.get_or_add_node_id(loc_prps)
        # Getting only the external links
        combin_inc_segs_p = []
        for lst in combin_inc_segs:
            for el in lst:
                combin_inc_segs_p.append(el)
        combin_external_inc_segs = [item for item, count in collections.Counter(combin_inc_segs_p).items() if count < 2]

        return combin_external_inc_segs, loc_prps, m_node_id

    # def merge_two_nodes(self, n_1: int, n_2: int):  # TODO: REMOVE
    #     #     find these two nodes and update everything that they reference or has referenced them
    #     #     propose the new location (midpoit)
    #     #     get a node id for that location
    #     #     merge their attribute including their incident sergments
    #     #     drop the mid divding segment, which is a segment with the two nodes conecting
    #
    #     node_1 = self.nodes_reversed_dict[f'{self.nodeid_to_reversedicindex[n_1]}']
    #     node_2 = self.nodes_reversed_dict[f'{self.nodeid_to_reversedicindex[n_2]}']
    #     loc_prps = self.midpoint(node_1.lon, node_1.lat, node_2.lon, node_2.lat)
    #     m_node_id = self.get_or_add_node_id(tuple(loc_prps))
    #     combin_inc_segs = list()
    #     for _node_ in [node_1, node_2]:
    #         for incid_seg in _node_.incident_segments:
    #             # to exclude internal links
    #             if (self.segments_dict[incid_seg]._nodes[0] in [n_1, n_2]) and \
    #                     (self.segments_dict[incid_seg]._nodes[-1] in [n_1, n_2]):
    #                 pass
    #             else:
    #
    #                 combin_inc_segs.append(incid_seg)
    #                 #         update the nodes in those incident segments with the new node
    #                 _new_node_list = []
    #                 for _n in self.segments_dict[incid_seg]._nodes:
    #                     if _n in [n_1, n_2]:
    #                         _new_node_list.append(m_node_id)
    #                     else:
    #                         _new_node_list.append(_n)
    #                 self.segments_dict[incid_seg]._nodes = list(set(_new_node_list))
    #         _new_dual_name_to_nodeids = {}
    #         for dual_name in _node_.dual_name_to_nodeid:
    #             if _node_.dual_name_to_nodeid[dual_name] in [n_1, n_2]:
    #                 pass
    #             else:
    #                 _new_dual_name_to_nodeids.update({
    #                     dual_name: _node_.dual_name_to_nodeid[dual_name]
    #                 })
    #
    #     self.nodes_reversed_dict[
    #         f'{float(loc_prps[0]):.15f}{float(loc_prps[1]):.15f}'
    #     ].dual_name_to_nodeid = _new_dual_name_to_nodeids
    #     self.nodes_reversed_dict[
    #         f'{float(loc_prps[0]):.15f}{float(loc_prps[1]):.15f}'
    #     ].incident_segments = list(set(combin_inc_segs))
    #     self.nodes_reversed_dict[
    #         f'{float(loc_prps[0]):.15f}{float(loc_prps[1]):.15f}'
    #     ].is_multinode_processed.append([n_1, n_2])
    #
    #     return m_node_id, loc_prps

    # def inc_seg_geo_for_multinodes(self, incid_seg_id, node_id):
    #     first_node = self.segments_dict[incid_seg_id]._nodes[0]
    #     last_node = self.segments_dict[incid_seg_id]._nodes[-1]
    #     if first_node == node_id:
    #         adj_incident_segment = [
    #             self.segments_dict[incid_seg_id]._nodes[0],
    #             self.segments_dict[incid_seg_id]._nodes[-1]
    #         ]
    #         incident_seg_geom = [
    #             [
    #                 self.nodes_reversed_dict[f"{self.nodeid_to_reversedicindex[adj_incident_segment[0]]}"].lon,
    #                 self.nodes_reversed_dict[f"{self.nodeid_to_reversedicindex[adj_incident_segment[0]]}"].lat
    #             ],
    #             [
    #                 self.nodes_reversed_dict[f"{self.nodeid_to_reversedicindex[adj_incident_segment[1]]}"].lon,
    #                 self.nodes_reversed_dict[f"{self.nodeid_to_reversedicindex[adj_incident_segment[1]]}"].lat
    #             ]
    #         ]
    #     elif last_node == node_id:
    #         adj_incident_segment = [
    #             self.segments_dict[incid_seg_id]._nodes[-1],
    #             self.segments_dict[incid_seg_id]._nodes[0]
    #         ]
    #         incident_seg_geom = [
    #             [
    #                 self.nodes_reversed_dict[f"{self.nodeid_to_reversedicindex[adj_incident_segment[0]]}"].lon,
    #                 self.nodes_reversed_dict[f"{self.nodeid_to_reversedicindex[adj_incident_segment[0]]}"].lat
    #             ],
    #             [
    #                 self.nodes_reversed_dict[f"{self.nodeid_to_reversedicindex[adj_incident_segment[1]]}"].lon,
    #                 self.nodes_reversed_dict[f"{self.nodeid_to_reversedicindex[adj_incident_segment[1]]}"].lat
    #             ]
    #         ]
    #     else:
    #
    #         incident_seg_geom = []
    #     return incident_seg_geom
