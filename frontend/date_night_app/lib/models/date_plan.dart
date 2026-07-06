class RestaurantPick {
  final String name;
  final double rating;
  final String priceLevel;
  final String address;
  final String description;
  final String vibeNotes;
  final String reservationInfo;
  final String? reservationUrl;
  final String? imageUrl;

  RestaurantPick({
    required this.name,
    required this.rating,
    required this.priceLevel,
    required this.address,
    required this.description,
    required this.vibeNotes,
    required this.reservationInfo,
    this.reservationUrl,
    this.imageUrl,
  });

  factory RestaurantPick.fromJson(Map<String, dynamic> json) {
    return RestaurantPick(
      name: json['name'] ?? '',
      rating: (json['rating'] ?? 0).toDouble(),
      priceLevel: json['price_level'] ?? '\$\$',
      address: json['address'] ?? '',
      description: json['description'] ?? '',
      vibeNotes: json['vibe_notes'] ?? '',
      reservationInfo: json['reservation_info'] ?? 'Check website',
      reservationUrl: json['reservation_url'],
      imageUrl: json['image_url'],
    );
  }
}

class DatePlanResponse {
  final RestaurantPick primaryPick;
  final RestaurantPick backupPick;
  final String talkingPoint;
  final String summary;

  DatePlanResponse({
    required this.primaryPick,
    required this.backupPick,
    required this.talkingPoint,
    required this.summary,
  });

  factory DatePlanResponse.fromJson(Map<String, dynamic> json) {
    return DatePlanResponse(
      primaryPick: RestaurantPick.fromJson(json['primary_pick']),
      backupPick: RestaurantPick.fromJson(json['backup_pick']),
      talkingPoint: json['talking_point'] ?? '',
      summary: json['summary'] ?? '',
    );
  }
}
