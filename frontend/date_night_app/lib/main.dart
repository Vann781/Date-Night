import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const DateNightApp());
}

class DateNightApp extends StatelessWidget {
  const DateNightApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Date Night',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFFE94560),
          brightness: Brightness.light,
          primary: const Color(0xFFE94560),
          onPrimary: Colors.white,
          primaryContainer: Color(0xFFFCE4EC),
          onPrimaryContainer: Color(0xFF7F1D2D),
          secondary: const Color(0xFF1A1A2E),
          onSecondary: Colors.white,
          secondaryContainer: Color(0xFFE8E8F0),
          onSecondaryContainer: Color(0xFF1A1A2E),
          tertiary: const Color(0xFFB07D4B),
          tertiaryContainer: Color(0xFFF5EDE4),
          onTertiaryContainer: Color(0xFF5C3D1E),
          surface: Colors.white,
          onSurface: const Color(0xFF1A1A2E),
          surfaceContainerHighest: Color(0xFFF5F5FA),
          outlineVariant: Color(0xFFE0E0E8),
        ),
        useMaterial3: true,
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: const Color(0xFFF5F5FA),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(14),
            borderSide: BorderSide.none,
          ),
          hintStyle: TextStyle(
            color: const Color(0xFF1A1A2E).withValues(alpha: 0.35),
          ),
        ),
        filledButtonTheme: FilledButtonThemeData(
          style: FilledButton.styleFrom(
            backgroundColor: const Color(0xFFE94560),
            foregroundColor: Colors.white,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(16),
            ),
          ),
        ),
        outlinedButtonTheme: OutlinedButtonThemeData(
          style: OutlinedButton.styleFrom(
            foregroundColor: const Color(0xFFE94560),
            side: const BorderSide(color: Color(0xFFE94560)),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(14),
            ),
          ),
        ),
        snackBarTheme: SnackBarThemeData(
          behavior: SnackBarBehavior.floating,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
        ),
      ),
      home: const HomeScreen(),
    );
  }
}
