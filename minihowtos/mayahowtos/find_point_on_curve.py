import maya.api.OpenMaya as om

def find_point_on_curve_to_point_by_distance(curve, to_point, distance, error_threshold = 1.0):

	sl = om.MSelectionList()
	sl.add(curve)
	curve_fn = om.MFnNurbsCurve(sl.getDagPath(0))

	u_begin = curve_fn.getParamAtPoint(om.MPoint(to_point), space = om.MSpace.kWorld)

	max_param = curve_fn.numCVs - curve_fn.degree

	arc_length = curve_fn.findLengthFromParam(max_param)
	u_increase = error_threshold / arc_length

	param_begin = u_begin * max_param

	p_ = curve_fn.getPointAtParam(param_begin, space = om.MSpace.kWorld)
	u_ = u_begin
	while u_ < 1:
		u_param = u_ * max_param
		p = curve_fn.getPointAtParam(u_param, space = om.MSpace.kWorld)
		length = (p - p_).length()
		if abs(length - distance) <= error_threshold:
			return p, u_
		u_ += u_increase

	return p, 1.0