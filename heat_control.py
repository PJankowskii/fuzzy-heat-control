from pyowm.owm import OWM
import math
import time
import os
from dotenv import load_dotenv


class TemperatureControl(object):
    def __init__(self):
        pass

    def get_forecast_temp(self):
        load_dotenv()
        owm = OWM(os.getenv('OWM'))
        mgr = owm.weather_manager()
        one_call = mgr.one_call(lat=54.1919, lon=16.1874)  # actual temperature in Koszalin,
        # (lat=-22.9390, lon=-43.2346) actual temperature in Rio de Janeiro
        day_temp = float(one_call.forecast_daily[0].temperature('celsius').get('day', None))
        print(day_temp)
        return day_temp

    def get_room_temp(self):
        list_inside_temp = []
        input_temp = float(input('Give the room temperature: '))
        if input_temp < -10:
            print("Temperature is too low!")
            exit()
        elif input_temp > 40:
            print("Temperature is too high!")
            exit()
        else:
            list_inside_temp.append(input_temp)
            return list_inside_temp

    def frozen_outside(self, outside_temp):
        if outside_temp > 0:
            return 0
        elif outside_temp < -10:
            return 1
        elif -10 <= outside_temp <= 0:
            return 0.5 * (1 + math.cos(math.pi * ((outside_temp - (-10)) / (0 - (-10)))))
        else:
            pass

    def cold_outside(self, outside_temp):
        if 5 < outside_temp < 6:
            return 1
        elif -1 <= outside_temp <= 5:
            return (outside_temp - (-1)) / (5 - (-1))
        elif 6 <= outside_temp <= 13:
            return (13 - outside_temp) / (13 - 6)
        else:
            return 0

    def heat_outside(self, outside_temp):
        if 12 < outside_temp <= 17:
            return (outside_temp - 12) / (17 - 12)
        elif 17 < outside_temp <= 21:
            return (21 - outside_temp) / (21 - 17)
        else:
            return 0

    def hot_outside(self, outside_temp):
        if 23 < outside_temp < 25:
            return 1
        elif 20 <= outside_temp <= 23:
            return (outside_temp - 20) / (23 - 20)
        elif 25 <= outside_temp <= 28:
            return (28 - outside_temp) / (28 - 25)
        else:
            return 0

    def very_hot_outside(self, outside_temp):
        if outside_temp < 27:
            return 0
        elif outside_temp > 30:
            return 1
        elif 27 <= outside_temp <= 30:
            return 0.5 * (1 - math.cos(math.pi * ((outside_temp - 27) / (30 - 27))))
        else:
            pass

    def very_cold_inside(self, list_inside):
        if list_inside[0] > 6:
            return 0
        elif list_inside[0] < 0:
            return 1
        elif 0 <= list_inside[0] <= 6:
            return 0.5 * (1 + math.cos(math.pi * ((list_inside[0] - 0) / (6 - 0))))
        else:
            pass

    def cold_inside(self, list_inside):
        if 7 < list_inside[0] < 10:
            return 1
        elif 5 <= list_inside[0] <= 7:
            return (list_inside[0] - 5) / (7 - 5)
        elif 10 <= list_inside[0] <= 19:
            return (19 - list_inside[0]) / (19 - 10)
        else:
            return 0

    def warm_inside(self, list_inside):
        if 20 < list_inside[0] < 21:
            return 1
        elif 18 <= list_inside[0] <= 20:
            return (list_inside[0] - 18) / (20 - 18)
        elif 21 <= list_inside[0] <= 23:
            return (23 - list_inside[0]) / (23 - 21)
        else:
            return 0

    def hot_inside(self, list_inside):
        if 24 < list_inside[0] < 25:
            return 1
        elif 22 <= list_inside[0] <= 24:
            return (list_inside[0] - 22) / (24 - 22)
        elif 25 <= list_inside[0] <= 27:
            return (27 - list_inside[0]) / (27 - 25)
        else:
            return 0

    def very_hot_inside(self, list_inside):
        if list_inside[0] < 26:
            return 0
        elif list_inside[0] > 30:
            return 1
        elif 26 <= list_inside[0] <= 30:
            return 0.5 * (1 - math.cos(math.pi * ((list_inside[0] - 26) / (30 - 26))))
        else:
            pass

    def fuzzy_rules(self, outside_temp, list_inside_temp):
        list_inside = list_inside_temp
        while outside_temp:
            time.sleep(1)
            print("***inside temperature***")
            print(list_inside)
            print("***inside temperature***")
            dict_list_of_minimum_conditioner = {
                "strong_cooling": [],
                "cooling": [],
                "off": [],
                "heating": [],
                "strong_heating": []
            }
            # temperatures_inside[0-very_cold, 1-cold, 2-warm, 3-hot, 4-very_hot]
            # temperatures_outside[0-frozen, 1-cold, 2-heat, 3-hot, 4-very_hot]
            temperatures_inside = [-10 <= list_inside[0] <= 6,
                                   5 <= list_inside[0] <= 19,
                                   18 <= list_inside[0] <= 23,
                                   22 <= list_inside[0] <= 27,
                                   26 <= list_inside[0] <= 40]
            temperatures_outside = [-20 <= outside_temp <= 0,
                                    -1 <= outside_temp <= 13,
                                    12 <= outside_temp <= 21,
                                    20 <= outside_temp <= 28,
                                    27 <= outside_temp <= 40]
            print(temperatures_inside[0], temperatures_inside[1], temperatures_inside[2], temperatures_inside[3],
                  temperatures_inside[4])
            print(temperatures_outside[0], temperatures_outside[1], temperatures_outside[2], temperatures_outside[3],
                  temperatures_outside[4])
            if temperatures_inside[0] and temperatures_outside[0]:
                # klimatyzator is mocne grzanie
                minimum = min(self.very_cold_inside(list_inside), self.frozen_outside(outside_temp))
                dict_list_of_minimum_conditioner["strong_heating"].append(minimum)
                print(minimum)
                print("mocne grzanie, very cold, frozen")
            if temperatures_inside[1] and temperatures_outside[0]:
                # klimatyzator is mocne grzanie
                minimum = min(self.cold_inside(list_inside), self.frozen_outside(outside_temp))
                dict_list_of_minimum_conditioner["strong_heating"].append(minimum)
                print(minimum)
                print("mocne grzanie, cold, frozen")
            if temperatures_inside[2] and temperatures_outside[0]:
                # klimatyzator is grzanie
                minimum = min(self.warm_inside(list_inside), self.frozen_outside(outside_temp))
                dict_list_of_minimum_conditioner["heating"].append(minimum)
                print(minimum)
                print("grzanie, warm, frozen")
            if temperatures_inside[3] and temperatures_outside[0]:
                # klimatyzator is wylacz
                minimum = min(self.hot_inside(list_inside), self.frozen_outside(outside_temp))
                dict_list_of_minimum_conditioner["off"].append(minimum)
                print(minimum)
                print("wylacz, hot, frozen")
            if temperatures_inside[4] and temperatures_outside[0]:
                # klimatyzator i wylacz
                minimum = min(self.very_hot_inside(list_inside), self.frozen_outside(outside_temp))
                dict_list_of_minimum_conditioner["off"].append(minimum)
                print(minimum)
                print("wylacz, very hot, frozen")
            if temperatures_inside[0] and temperatures_outside[1]:
                minimum = min(self.very_cold_inside(list_inside), self.cold_outside(outside_temp))
                dict_list_of_minimum_conditioner["strong_heating"].append(minimum)
                print(minimum)
                print("mocne grzanie, very cold, cold")
            if temperatures_inside[1] and temperatures_outside[1]:
                # klimatyzator is grzanie
                minimum = min(self.cold_inside(list_inside), self.cold_outside(outside_temp))
                dict_list_of_minimum_conditioner["heating"].append(minimum)
                print(minimum)
                print("grzanie, cold, cold")
            if temperatures_inside[2] and temperatures_outside[1]:
                # klimatyzator is wylacz
                minimum = min(self.warm_inside(list_inside), self.cold_outside(outside_temp))
                dict_list_of_minimum_conditioner["off"].append(minimum)
                print(minimum)
                print("wylacz, warm, cold")
            if temperatures_inside[3] and temperatures_outside[1]:
                # klimatyzator is wylacz
                minimum = min(self.hot_inside(list_inside), self.cold_outside(outside_temp))
                dict_list_of_minimum_conditioner["off"].append(minimum)
                print(minimum)
                print("wylacz, hot, cold")
            if temperatures_inside[4] and temperatures_outside[1]:
                # klimatyzator i chlodzenie
                minimum = min(self.very_hot_inside(list_inside), self.cold_outside(outside_temp))
                dict_list_of_minimum_conditioner["cooling"].append(minimum)
                print(minimum)
                print("chlodzenie, very hot, cold")
            if temperatures_inside[0] and temperatures_outside[2]:
                # klimatyzator is grzanie
                minimum = min(self.very_cold_inside(list_inside), self.heat_outside(outside_temp))
                dict_list_of_minimum_conditioner["heating"].append(minimum)
                print(minimum)
                print("grzanie, very cold, heat")
            if temperatures_inside[1] and temperatures_outside[2]:
                # klimatyzator is grzanie
                minimum = min(self.cold_inside(list_inside), self.heat_outside(outside_temp))
                dict_list_of_minimum_conditioner["heating"].append(minimum)
                print(minimum)
                print("grzanie,  cold, heat")
            if temperatures_inside[2] and temperatures_outside[2]:
                # klimatyzator is wylacz
                minimum = min(self.warm_inside(list_inside), self.heat_outside(outside_temp))
                dict_list_of_minimum_conditioner["off"].append(minimum)
                print(minimum)
                print("wylacz, warm, heat")
            if temperatures_inside[3] and temperatures_outside[2]:
                # klimatyzator is chlodzenie
                minimum = min(self.hot_inside(list_inside), self.heat_outside(outside_temp))
                dict_list_of_minimum_conditioner["cooling"].append(minimum)
                print(minimum)
                print("chlodzenie, hot, heat")
            if temperatures_inside[4] and temperatures_outside[2]:
                # klimatyzator i chlodzenie
                minimum = min(self.very_hot_inside(list_inside), self.heat_outside(outside_temp))
                dict_list_of_minimum_conditioner["cooling"].append(minimum)
                print(minimum)
                print("chlodzenie, very hot, heat")
            if temperatures_inside[0] and temperatures_outside[3]:
                # klimatyzator is grzanie
                minimum = min(self.very_cold_inside(list_inside), self.hot_outside(outside_temp))
                dict_list_of_minimum_conditioner["heating"].append(minimum)
                print(minimum)
                print("grzanie, very cold, hot")
            if temperatures_inside[1] and temperatures_outside[3]:
                # klimatyzator is wylacz
                minimum = min(self.cold_inside(list_inside), self.hot_outside(outside_temp))
                dict_list_of_minimum_conditioner["off"].append(minimum)
                print(minimum)
                print("wylacz,  cold, hot")
            if temperatures_inside[2] and temperatures_outside[3]:
                # klimatyzator is wylacz
                minimum = min(self.warm_inside(list_inside), self.hot_outside(outside_temp))
                dict_list_of_minimum_conditioner["off"].append(minimum)
                print(minimum)
                print("wylacz, warm, hot")
            if temperatures_inside[3] and temperatures_outside[3]:
                # klimatyzator is chlodzenie
                minimum = min(self.hot_inside(list_inside), self.hot_outside(outside_temp))
                dict_list_of_minimum_conditioner["cooling"].append(minimum)
                print(minimum)
                print("chlodzenie, hot, hot")
            if temperatures_inside[4] and temperatures_outside[3]:
                # klimatyzator i chlodzenie
                minimum = min(self.very_hot_inside(list_inside), self.hot_outside(outside_temp))
                dict_list_of_minimum_conditioner["cooling"].append(minimum)
                print(minimum)
                print("chlodzenie, very hot, hot")
            if temperatures_inside[0] and temperatures_outside[4]:
                # klimatyzator is wylacz
                minimum = min(self.very_cold_inside(list_inside), self.very_hot_outside(outside_temp))
                dict_list_of_minimum_conditioner["off"].append(minimum)
                print(minimum)
                print("wylacz, very cold, very hot")
            if temperatures_inside[1] and temperatures_outside[4]:
                # klimatyzator is wylacz
                minimum = min(self.cold_inside(list_inside), self.very_hot_outside(outside_temp))
                dict_list_of_minimum_conditioner["off"].append(minimum)
                print(minimum)
                print("wylacz,  cold, very hot")
            if temperatures_inside[2] and temperatures_outside[4]:
                # klimatyzator is chlodzenie
                minimum = min(self.warm_inside(list_inside), self.very_hot_outside(outside_temp))
                dict_list_of_minimum_conditioner["cooling"].append(minimum)
                print(minimum)
                print("chlodzenie, warm, very hot")
            if temperatures_inside[3] and temperatures_outside[4]:
                # klimatyzator is mocne chlodzenie
                minimum = min(self.hot_inside(list_inside), self.very_hot_outside(outside_temp))
                dict_list_of_minimum_conditioner["strong_cooling"].append(minimum)
                print(minimum)
                print("mocne chlodzenie, hot, very hot")
            if temperatures_inside[4] and temperatures_outside[4]:
                # klimatyzator i mocne chlodzenie
                minimum = min(self.very_hot_inside(list_inside), self.very_hot_outside(outside_temp))
                dict_list_of_minimum_conditioner["strong_cooling"].append(minimum)
                print(minimum)
                print("mocne chlodzenie, very hot, very hot")

            max_value = max(i for v in dict_list_of_minimum_conditioner.values() for i in v)
            print("!!sprawdzane dicta i najwiekszej wartosci!!")
            print(dict_list_of_minimum_conditioner)
            print(max_value)
            print("!!koniec sprawdzania wartosci!!")

            if max_value in dict_list_of_minimum_conditioner.get("strong_cooling"):
                list_inside[0] -= 2.0
                # print("print w strong_cooling")
                # print(list_inside[0])
                if max_value not in dict_list_of_minimum_conditioner.get("strong_cooling"):
                    break

            elif max_value in dict_list_of_minimum_conditioner.get("cooling"):
                list_inside[0] -= 1.0
                # print("print w cooling")
                # print(list_inside[0])
                if max_value not in dict_list_of_minimum_conditioner.get("cooling"):
                    break

            elif max_value in dict_list_of_minimum_conditioner.get("off"):
                if temperatures_outside[0] or temperatures_outside[1]:
                    time.sleep(1)
                    list_inside[0] -= 1.0
                    # print("print w off minus")
                    # print(list_inside[0])
                elif temperatures_outside[3] or temperatures_outside[4]:
                    time.sleep(1)
                    list_inside[0] += 1.0
                    # print("print w off plus")
                    # print(list_inside[0])
                elif temperatures_outside[2] and max_value not in dict_list_of_minimum_conditioner.get("off"):
                    break

            elif max_value in dict_list_of_minimum_conditioner.get("heating"):
                list_inside[0] += 1.0
                # print("print w heating")
                # print(list_inside[0])
                if max_value not in dict_list_of_minimum_conditioner.get("heating"):
                    break

            elif max_value in dict_list_of_minimum_conditioner.get("strong_heating"):
                list_inside[0] += 2.0
                # print("print w strong_heating")
                # print(list_inside[0])
                if max_value not in dict_list_of_minimum_conditioner.get("strong_heating"):
                    break
        return list_inside


if __name__ == '__main__':
    temperature_control = TemperatureControl()
    outside_temp = temperature_control.get_forecast_temp()
    list_inside_temp = temperature_control.get_room_temp()

    temperature_control.frozen_outside(outside_temp)
    temperature_control.cold_outside(outside_temp)
    temperature_control.heat_outside(outside_temp)
    temperature_control.hot_outside(outside_temp)
    temperature_control.very_hot_outside(outside_temp)

    list_inside = temperature_control.fuzzy_rules(outside_temp, list_inside_temp)

    temperature_control.very_cold_inside(list_inside)
    temperature_control.cold_inside(list_inside)
    temperature_control.warm_inside(list_inside)
    temperature_control.hot_inside(list_inside)
    temperature_control.very_hot_inside(list_inside)
