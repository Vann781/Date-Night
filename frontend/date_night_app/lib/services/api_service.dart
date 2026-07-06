import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/date_plan.dart';

class ApiService {
  // 10.0.2.2 = Android emulator → host machine
  // Change to your machine's IP if testing on a physical device
  static const String _baseUrl = 'http://10.0.2.2:5000/api';

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
