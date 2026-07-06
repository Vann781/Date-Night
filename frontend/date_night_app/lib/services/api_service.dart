import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/date_plan.dart';

class ApiService {
  static const String _baseUrl = 'https://date-night-ky1n.onrender.com/api';

  static Future<DatePlanResponse> planDate({
    required String vibe,
    String cuisine = '',
    String budget = '\$\$',
    String location = '',
  }) async {
    final url = Uri.parse('$_baseUrl/plan-date');

    final response = await http
        .post(
          url,
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({
            'vibe': vibe,
            'cuisine': cuisine,
            'budget': budget,
            'location': location,
          }),
        )
        .timeout(const Duration(seconds: 60));

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return DatePlanResponse.fromJson(data);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['error'] ?? 'Something went wrong');
    }
  }
}
