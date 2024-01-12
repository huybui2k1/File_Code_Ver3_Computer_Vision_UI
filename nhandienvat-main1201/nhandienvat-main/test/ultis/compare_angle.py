from components.match_pattern import match_pattern


def compare_angle(point,minus_sub_angles,plus_sub_angles, gray_img, template_gray, bboxes, angle, method,result_queue ):
    minus_pointer, plus_pointer = 0,0
    exactly_minus, exactly_plus = 0, 0
    high_point_minus, high_point_plus = point, point
    bestAngle,bestPoint = 0,0

    while minus_pointer < len(minus_sub_angles)  or plus_pointer < len(plus_sub_angles):
        if minus_sub_angles[minus_pointer] > 360:
            init_angle = 360 - minus_sub_angles[minus_pointer]
            point_minus = match_pattern(gray_img, template_gray, bboxes, init_angle, method)
        else:
            init_angle = minus_sub_angles[minus_pointer]
            point_minus = match_pattern(gray_img, template_gray, bboxes, init_angle, method)
        if plus_sub_angles[plus_pointer] > 360:
            init_angle = 360 - plus_sub_angles[plus_pointer]
            point_plus = match_pattern(gray_img, template_gray, bboxes, plus_sub_angles[plus_pointer], method)
        else:
            init_angle = plus_sub_angles[plus_pointer]
            point_plus = match_pattern(gray_img, template_gray, bboxes, plus_sub_angles[plus_pointer], method)       
        
        if point_minus >= high_point_minus:
            if minus_sub_angles[minus_pointer] >= 360:
                exactly_minus = minus_sub_angles[minus_pointer] - 360
            else:
                exactly_minus = minus_sub_angles[minus_pointer]
            if point_minus > bestPoint:
                bestAngle = exactly_minus
                bestPoint = point_minus
            high_point_minus = point_minus
        
        if point_plus >= high_point_plus:
            if plus_sub_angles[plus_pointer] >= 360:
                exactly_plus = plus_sub_angles[plus_pointer] - 360
            else:
                exactly_plus = plus_sub_angles[minus_pointer]
            if point_plus > bestPoint:
                bestAngle = exactly_plus
                bestPoint = point_plus
            high_point_plus = point_plus
        
        minus_pointer = minus_pointer + 1
        plus_pointer = plus_pointer + 1
        # print("---------------------------------------")
    if bestPoint < point:
        bestAngle = angle
    if bestAngle > 270:
        bestAngle = (180 - (360- bestAngle))
    # transfer angle of 6-axis to angle of tool
    if bestAngle >= 90:
        bestAngle = bestAngle - 90
    else :
        bestAngle = 90 + bestAngle
    result_queue.append((-bestAngle, bestPoint))
    return bestAngle, bestPoint

#kiểm tra từng phần tử minus_sub_angles,plus_sub_angles, lấy angle mà có số điểm cao nhất 


def compare_angle_test(point,minus_sub_angles,plus_sub_angles, gray_img, template_gray, bboxes, angle, method,result_queue ):
    try:

        minus_pointer, plus_pointer = 0,0
        exactly_minus, exactly_plus = 0, 0
        high_point_minus, high_point_plus = point, point
        bestAngle,bestPoint = 0,0

        while minus_pointer < len(minus_sub_angles)  or plus_pointer < len(plus_sub_angles):
            if minus_sub_angles[minus_pointer] > 360:
                init_angle_minus = 360 - minus_sub_angles[minus_pointer]
                point_minus = match_pattern(gray_img, template_gray, bboxes, init_angle_minus, method)
            else:
                init_angle_minus = minus_sub_angles[minus_pointer]
                point_minus = match_pattern(gray_img, template_gray, bboxes, init_angle_minus, method)
            if plus_sub_angles[plus_pointer] > 360:
                init_angle_plus = 360 - plus_sub_angles[plus_pointer]
                point_plus = match_pattern(gray_img, template_gray, bboxes, init_angle_plus, method)
            else:
                init_angle_plus = plus_sub_angles[plus_pointer]
                point_plus = match_pattern(gray_img, template_gray, bboxes, init_angle_plus, method)       
            # print("angle_minus - angle - plus: ",init_angle_minus, init_angle_plus)
            # print("minus - plus init: ",point_minus,point_plus)
            if point_minus >= high_point_minus:
                if minus_sub_angles[minus_pointer] >= 360:
                    exactly_minus = minus_sub_angles[minus_pointer] - 360
                else:
                    exactly_minus = minus_sub_angles[minus_pointer]
                if point_minus > bestPoint:
                    bestAngle = exactly_minus
                    bestPoint = point_minus
                high_point_minus = point_minus
            
            if point_plus >= high_point_plus:
                if plus_sub_angles[plus_pointer] >= 360:
                    exactly_plus = plus_sub_angles[plus_pointer] - 360
                else:
                    exactly_plus = plus_sub_angles[minus_pointer]
                if point_plus > bestPoint:
                    bestAngle = exactly_plus
                    bestPoint = point_plus
                high_point_plus = point_plus
            minus_pointer = minus_pointer + 1
            plus_pointer = plus_pointer + 1
            # print("---------------------------------------")
        if bestPoint < point:
            bestAngle = angle
        if bestAngle > 270:
            bestAngle = (180 - (360- bestAngle))
        print("best angle - point: ",bestAngle,bestPoint)
        # transfer angle of 6-axis to angle of tool
        if bestAngle >= 90:
            bestAngle = bestAngle - 90
        else :
            bestAngle = 90 + bestAngle
        # print("************************************************************************")
        
        result_queue.append((-bestAngle, bestPoint))
        return bestAngle, bestPoint
    except Exception as e:
        print(e)