from numpy import array

def cal_Q_score(results):
    proportion = array([results['sky'],results['building'],results['road'],results['sidewalk'],results['wall'],results['fence'],results['vegetation'],results['terrain']])
    Q1_weight = array([2.8426,1.3165,2.7089,2.1543,-1.6936,2.1222,4.735,6.6595])
    Q2_weight = array([0.5196,0,1.8506,-1.3083,0,0.8828,1.9856,4.4898])
    Q3_weight = array([1.2753,0,3.3066,0,0,0,3.0284,5.0464])
    Q4_weight = array([-1.2681,0,0.6857,2.9852,-3.0187,0,1.84,3.5054])
    Q5_weight = array([1.2263,0,2.5418,2.1126,-3.3077,2.003,3.4417,6.2069])
    Q6_weight = array([-2.7932,0,-2.7014,-2.0931,0,-0.9912,-2.2465,-3.535])
    Q_bias = array([1.7093,3.3772,2.4165,4.1416,2.5401,6.8242])
    Q_score = array([sum(proportion*Q1_weight),sum(proportion*Q2_weight),sum(proportion*Q3_weight),sum(proportion*Q4_weight),sum(proportion*Q5_weight),sum(proportion*Q6_weight)])
    Q_score = Q_score + Q_bias
    Q_score = {'relaxed':round(Q_score[0],2),'focused':round(Q_score[1],2),'motivated':round(Q_score[2],2),'social':round(Q_score[3],2),'happy':round(Q_score[4],2),'depressive':round(Q_score[5],2)}
    return Q_score