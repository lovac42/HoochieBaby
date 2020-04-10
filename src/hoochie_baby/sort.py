# -*- coding: utf-8 -*-
# Copyright: (C) 2018-2020 Lovac42
# Support: https://github.com/lovac42/HoochieBaby
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


CUSTOM_SORT = {
  0:["None (Shuffled)", "order by due, random()"],

# == User Config =========================================

  1:["Young first",  "order by ivl asc, random()"],
  2:["Mature first", "order by ivl desc, random()"],
  3:["Low reps",     "order by reps asc, random()"],
  4:["High reps",    "order by reps desc, random()"],
  5:["Low ease factor",  "order by factor asc, random()"],
  6:["High ease factor", "order by factor desc, random()"],
  7:["Low lapses",   "order by lapses asc, random()"],
  8:["High lapses",  "order by lapses desc, random()"],
  9:["Overdues",     "order by due asc, random()"],
 10:["Dues",         "order by due desc, random()"],

# == End Config ==========================================

 11:["Unrestricted Random (HighCPU)",  "order by random()"]
}
