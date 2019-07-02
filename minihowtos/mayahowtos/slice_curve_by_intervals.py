import maya.api.OpenMaya as om


def slice_curve_by_intervals(curve, intervals, error_threshold = 0.01, begin_at_param = 0, use_arc_length = False):

	sl = om.MSelectionList()
	sl.add(curve)
	curve_fn = om.MFnNurbsCurve(sl.getDagPath(0))

	# use max_param/numSpans to obtain curve length for step size approximation
	# we use half of error_threshold to estimate step size
	max_param = curve_fn.numSpans
	curve_length = curve_fn.findLengthFromParam(max_param)
	u_step = max_param * (0.5 * error_threshold) / curve_length

	# we could use either arc length or linear distane func to compute the distance 
	arc_len_func = lambda (s, t): curve_fn.findLengthFromParam(t) - curve_fn.findLengthFromParam(s)
	lin_dist_func = lambda (s, t): (curve_fn.getPointAtParam(t) - curve_fn.getPointAtParam(s)).length()
	dist_func = arc_len_func if use_arc_length else lin_dist_func

	# loop through intervals to find start and end points for each segment
	segments = []
	u_ = begin_at_param
	for distance in intervals:
		
		u_0 = u_
		u_ += u_step

		while u_ <= max_param:

			if abs(dist_func((u_0, u_)) - distance) < error_threshold:
				segments.append((curve_fn.getPointAtParam(u_0), curve_fn.getPointAtParam(u_)))
				break

			u_ += u_step

	return segments
