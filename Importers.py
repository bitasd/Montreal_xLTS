import pandas
import geopandas
from typing import List, Dict
from Segments import Segment_


class Mixin:
    def second_order_import(self, node_based_data_inv: list):
        nodes_ids = list()
        nodes_lons = list()
        nodes_lats = list()
        for node_d in self.nodes_reversed_dict:
            if len(self.nodes_reversed_dict[f"{node_d}"].incident_segments) > 2:
                nodes_ids.append(self.nodes_reversed_dict[f"{node_d}"].id)
                nodes_lons.append(self.nodes_reversed_dict[f"{node_d}"].lon)
                nodes_lats.append(self.nodes_reversed_dict[f"{node_d}"].lat)
        nodeddf = pandas.DataFrame({
            'node_id': nodes_ids,
            'node_lon': nodes_lons,
            'node_lat': nodes_lats
        })
        nodes_point_geodf = geopandas.GeoDataFrame(
            nodeddf,
            geometry=geopandas.points_from_xy(
                nodeddf.node_lon,
                nodeddf.node_lat
            )
        )
        nodes_point_geodf.set_crs(
            epsg=4326,
            inplace=True
        )
        for node_based_data in node_based_data_inv:
            try:
                node_based_data['geodataframe']['geometry'] = node_based_data[
                    'geodataframe'
                ].geometry.buffer(
                    self._buffersize
                )
            except ValueError:
                print('ValueError when buffering nodes for ', node_based_data['name'])
                pass
            # instead of this doing it one by one (turned out very costly) make a geodatafram out of all the nodes
            # then intersect everythin and look up with loc

            nodes_with_importedattributes = geopandas.sjoin(
                nodes_point_geodf,
                node_based_data['geodataframe'],
                how="inner",
                op='intersects'
            )
            for node_d in self.nodes_reversed_dict:
                if len(self.nodes_reversed_dict[f"{node_d}"].incident_segments) > 2:
                    node__with_importedattributes = nodes_with_importedattributes.loc[
                        nodes_with_importedattributes['node_id'] == self.nodes_reversed_dict[f"{node_d}"].id,]
                    if len(node__with_importedattributes) > 0:
                        for n_ in range(len(node__with_importedattributes)):
                            self.nodes_reversed_dict[f"{node_d}"].has_other_attributes.append(
                                {
                                    f'{node_based_data["name"]}_{node_based_data["field_to_fetch"]}_{n_}':
                                        node__with_importedattributes[node_based_data['field_to_fetch']].values[n_]
                                }
                            )
                    else:
                        self.nodes_reversed_dict[f"{node_d}"].has_other_attributes.append(
                            {
                                f'{node_based_data["name"]}':
                                    None
                            }
                        )

    def first_order_import(
            self,
            streets: geopandas.GeoDataFrame,
            field_val_spec_dual_cargwy: Dict[str, str] = None,
            field_street_name=None
    ):
        if field_val_spec_dual_cargwy is None:
            field_val_spec_dual_cargwy = {'ONEWAY': 'DIVIDED'}
        self.field_val_spec_dual_cargwy = field_val_spec_dual_cargwy
        self.field_street_name = field_street_name
        _attrs = list(streets.columns)
        del _attrs[-1]
        for i in range(len(streets)):
            _street = streets.loc[streets.index == i, ]
            self._in_seg_id += 1
            seg = Segment_(self._in_seg_id, [], {})
            for streetM in _street['geometry']:
                for street in streetM:
                    for vert_index in range(len(list(street.coords))):
                        vert = list(street.coords)[vert_index]
                        ndid = self.get_or_add_node_id(vert)
                        self.nodeid_to_reversedicindex.update({
                            ndid: f"{float(vert[0]):.15f}{float(vert[1]):.15f}"
                        })
                        seg._nodes.append(ndid)
                        if (vert_index == 0) or (vert_index == len(list(street.coords)) - 1):
                            self.save_incident_segment(ndid, self._in_seg_id)
            for _attr in _attrs:
                seg._attributes.update({
                    f"{_attr}": _street[f'{_attr}'].values[0]
                })
            # having the dictionary will be making the process faster but will be very memory costly
            # some kind of logic for this comprimise is needed
            self.segments_dict.update({
                self._in_seg_id: seg
            })
