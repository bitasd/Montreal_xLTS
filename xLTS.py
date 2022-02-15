
class Mixin:

    # Attributes are for the road being crossed
    def xLTS_calc(self,
                  control,
                  pocketTrig,
                  xdistsig,
                  twostage,
                  linktype,
                  speed_limit,
                  xllestop,
                  adt,
                  nblane,
                  vislim,
                  c_sens_cir,
                  ramptrig,
                  feuxvelo,
                  sasvelo,
                  volrt,
                  avancflech
                  ):

        if c_sens_cir == 0:  # crossing a twoway street
            nbr_lane = 2 * nblane
        else:
            nbr_lane = nblane
        # if no trigger for lts 2 or 3, it would be 1
        xlts = 1

        # 4 way stop
        if control == 'Stop4':
            xlts = 1
        # Signalized
        elif control == 'Signal':
            # Trigger lts = 2
            # No bike signal and sasvelo and volrt
            # xdist > 30m, multistage x, pocket bikelane, mixing zone (we dont have 'em:)
            if feuxvelo == 0:
                if (sasvelo > 0 or avancflech > 0) and volrt > 240:
                    xlts = 2
                elif volrt > 120:
                    xlts = 2
                else:
                    pass

            if xdistsig > 30 or twostage > 0 or pocketTrig == 2:
                xlts = 2
            # Trigger lts = 3
            elif pocketTrig == 3:
                xlts = 3
            else:
                pass

        # Unsignalized
        else:
            # trail
            if linktype != 'Road':

                # Table A -- Where a stand-alone trail crosses a 2-lane road and bikes are expected to stop
                # crossing two-lane roads
                if nbr_lane == 1:
                    if adt <= 8000:
                        if speed_limit <= 62:
                            xlts = 1
                        else:

                            xlts = self.lts_b(speed_limit, xllestop, adt, nbr_lane)
                    else:
                        if speed_limit <= 46:
                            if xllestop > 0:
                                xlts = 1
                            else:
                                xlts = self.lts_b(speed_limit, xllestop, adt, nbr_lane)

                # trail crossing a multilane
                # Table B
                else:
                    xlts = self.lts_b(speed_limit, xllestop, adt, nbr_lane)

            # not a trail
            else:
                xlts = self.lts_b(speed_limit, xllestop, adt, nbr_lane)

        # Blind Entry
        if vislim > 0:
            xlts = max(2, xlts)
        else:
            pass
        # Ramp conflict
        xlts = max(xlts, ramptrig)
        # print('xlts is ', xlts)
        return xlts

    @staticmethod
    def lts_b(speed_limit, xllestop, adt, nbr_lane):
        # LTS when  85-p speed on the road being crossed <= 62 km/h
        if speed_limit <= 62:
            # Roads w/ X island
            if 0 < xllestop < 1.8:
                if adt <= 6000:
                    xlts_b = 1
                elif adt <= 24000:
                    xlts_b = 2
                else:
                    xlts_b = 3
            elif xllestop >= 1.8:
                if adt <= 12000:
                    xlts_b = 1
                elif adt <= 24000:
                    xlts_b = 2
                else:
                    xlts_b = 3
            elif nbr_lane in [1, 2, 3]:
                if adt <= 9000:
                    xlts_b = 1
                elif adt <= 17000:
                    xlts_b = 2
                else:
                    xlts_b = 3
            elif nbr_lane >= 4:
                if adt <= 6000:
                    xlts_b = 1
                elif adt <= 12000:
                    xlts_b = 2
                elif adt <= 19000:
                    xlts_b = 3
                else:
                    xlts_b = 4
            else:
                xlts_b = 1001

        # LTS when  85-p speed on the road being crossed > 62 km/h
        else:

            # Roads w/ X island
            if 0 < xllestop < 1.8:
                if adt <= 17000:
                    xlts_b = 2
                else:
                    xlts_b = 3
            elif xllestop >= 1.8:
                if adt <= 8000:
                    xlts_b = 1
                elif adt <= 17000:
                    xlts_b = 2
                else:
                    xlts_b = 3
            elif nbr_lane in [1, 2, 3]:
                if adt <= 6000:
                    xlts_b = 1
                elif adt <= 12000:
                    xlts_b = 2
                elif adt <= 18000:
                    xlts_b = 3
                else:
                    xlts_b = 4
            elif nbr_lane >= 4:
                if adt <= 10000:
                    xlts_b = 2
                elif adt <= 14000:
                    xlts_b = 3
                else:
                    xlts_b = 4
            else:
                xlts_b = 1002

        return xlts_b
