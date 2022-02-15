import geopandas
import xLTS


class xLTSAgent(
    xLTS.Mixin
):

    # TODO: CHANGE THE DIRECTORY FOR THE INPUT, YOU CAN SPECIFY THE INPUT TYPE (SHP, GPKG, ETC.)
    def run(self):
        base_gdf = geopandas.read_file('C:\\Users\\bitas\\folders\\Research\\Montreal\\mojde\\cross_dec16.gpkg'
                                       ).fillna(0)

        to_int_cols = ['ADT', 'Q85', 'NBLane', 'XDistSig', 'VisLim', 'RampTrig',
                       'TwoStage', 'PocketTrig', 'FeuxVelo', 'SAS_Velo', 'AvancFlech']
        to_float_cols = ['VolRT', 'XileStop', 'c_SENS_CIR']

        base_gdf[to_int_cols] = base_gdf[to_int_cols].astype(int)
        base_gdf[to_float_cols] = base_gdf[to_float_cols].astype(float)

        print(len(base_gdf), "CROSSINGS")

        base_gdf['xlts'] = base_gdf.apply(lambda row: self.xLTS_calc(
            control=row['Control'],
            pocketTrig=row['PocketTrig'],
            xdistsig=row['XDistSig'],
            twostage=row['TwoStage'],
            linktype=row['LinkType'],
            speed_limit=row['Q85'],
            xllestop=row['XileStop'],
            adt=row['ADT'],
            nblane=row['NBLane'],
            vislim=row['VisLim'],
            c_sens_cir=row['c_SENS_CIR'],
            ramptrig=row['RampTrig'],
            feuxvelo=row['FeuxVelo'],
            sasvelo=row['SAS_Velo'],
            volrt=row['VolRT'],
            avancflech=row['AvancFlech']
        ), axis=1)

        return base_gdf


xa = xLTSAgent()
lts_df = xa.run()
lts_df = lts_df.rename(columns={'f_ONEWAY': 'f_DIVIDED', 't_ONEWAY': 't_DIVIDED', 'c_ONEWAY': 'c_DIVIDED'})
# TODO: CHANGE THE DIRECTORY FOR THE OUTPUT, YOU CAN SPECIFY THE OUTPUT TYPE (SHP, GPKG, ETC.)
lts_df.to_file('C:\\Users\\bitas\\folders\\Research\\Montreal\\codes\\intersection\\Nov1\\xLTS_2.geojson',
               driver='GeoJSON')
# lts_df.to_file('C:\\Users\\bitas\\folders\\Research\\Montreal\\codes\\intersection\\Nov1\\xLTS.gpkg',
#                layer='xLTS_2',
#                driver='GPKG')
