import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../widgets/budget_selector.dart';
import 'results_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _vibeController = TextEditingController();
  final _cuisineController = TextEditingController();
  final _locationController = TextEditingController();
  String _selectedBudget = '\$\$';
  bool _isLoading = false;

  @override
  void dispose() {
    _vibeController.dispose();
    _cuisineController.dispose();
    _locationController.dispose();
    super.dispose();
  }

  Future<void> _planDate() async {
    if (_vibeController.text.trim().isEmpty) {
      _showError('Please describe the vibe you\'re going for');
      return;
    }

    setState(() => _isLoading = true);

    try {
      final result = await ApiService.planDate(
        vibe: _vibeController.text.trim(),
        cuisine: _cuisineController.text.trim(),
        budget: _selectedBudget,
        location: _locationController.text.trim(),
      );

      if (!mounted) return;

      Navigator.push(
        context,
        PageRouteBuilder(
          pageBuilder: (_, _, _) => ResultsScreen(result: result),
          transitionsBuilder: (_, animation, _, child) => SlideTransition(
            position: Tween<Offset>(begin: const Offset(1, 0), end: Offset.zero)
                .animate(
                  CurvedAnimation(
                    parent: animation,
                    curve: Curves.easeOutCubic,
                  ),
                ),
            child: child,
          ),
        ),
      );
    } catch (e) {
      _showError(e.toString().replaceFirst('Exception: ', ''));
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  void _showError(String message) {
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        margin: const EdgeInsets.all(16),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final size = MediaQuery.of(context).size;

    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: EdgeInsets.fromLTRB(24, size.height * 0.06, 24, 32),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _Header(),
              SizedBox(height: size.height * 0.04),
              _InputSection(
                icon: Icons.auto_awesome,
                title: 'Vibe',
                subtitle: 'Describe the mood you want',
                child: TextField(
                  controller: _vibeController,
                  maxLines: 3,
                  decoration: _inputDecoration(
                    hint: 'e.g. romantic but not stuffy...',
                  ),
                  textCapitalization: TextCapitalization.sentences,
                ),
              ),
              const SizedBox(height: 20),
              _InputSection(
                icon: Icons.restaurant,
                title: 'Cuisine',
                subtitle: 'Any preference? (optional)',
                child: TextField(
                  controller: _cuisineController,
                  decoration: _inputDecoration(hint: 'e.g. Italian, Japanese'),
                  textCapitalization: TextCapitalization.sentences,
                ),
              ),
              const SizedBox(height: 20),
              _InputSection(
                icon: Icons.attach_money,
                title: 'Budget',
                subtitle: 'Pick your price range',
                child: BudgetSelector(
                  selected: _selectedBudget,
                  onChanged: (v) => setState(() => _selectedBudget = v),
                ),
              ),
              const SizedBox(height: 20),
              _InputSection(
                icon: Icons.location_on,
                title: 'Location',
                subtitle: 'Area or distance preference (optional)',
                child: TextField(
                  controller: _locationController,
                  decoration: _inputDecoration(
                    hint: 'e.g. downtown, within 15 mins',
                  ),
                  textCapitalization: TextCapitalization.sentences,
                ),
              ),
              const SizedBox(height: 36),
              SizedBox(
                width: double.infinity,
                height: 56,
                child: FilledButton(
                  onPressed: _isLoading ? null : _planDate,
                  style: FilledButton.styleFrom(
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16),
                    ),
                    elevation: 0,
                  ),
                  child: _isLoading
                      ? SizedBox(
                          width: 24,
                          height: 24,
                          child: CircularProgressIndicator(
                            strokeWidth: 2.5,
                            color: theme.colorScheme.onPrimary,
                          ),
                        )
                      : Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(Icons.auto_awesome, size: 20),
                            const SizedBox(width: 10),
                            Text(
                              'Plan My Date',
                              style: theme.textTheme.titleMedium?.copyWith(
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                          ],
                        ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  InputDecoration _inputDecoration({required String hint}) {
    return InputDecoration(
      hintText: hint,
      filled: true,
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(14),
        borderSide: BorderSide.none,
      ),
      contentPadding: const EdgeInsets.all(16),
    );
  }
}

class _Header extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          width: 48,
          height: 48,
          decoration: BoxDecoration(
            color: theme.colorScheme.primaryContainer,
            borderRadius: BorderRadius.circular(14),
          ),
          child: Icon(
            Icons.nights_stay,
            color: theme.colorScheme.onPrimaryContainer,
            size: 24,
          ),
        ),
        const SizedBox(height: 20),
        Text(
          'Date Night',
          style: theme.textTheme.headlineLarge?.copyWith(
            fontWeight: FontWeight.bold,
            height: 1.1,
          ),
        ),
        const SizedBox(height: 8),
        Text(
          'Tell me what you\'re in the mood for,\nand I\'ll plan the perfect evening.',
          style: theme.textTheme.bodyLarge?.copyWith(
            color: theme.colorScheme.onSurface.withValues(alpha: 0.6),
            height: 1.4,
          ),
        ),
      ],
    );
  }
}

class _InputSection extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final Widget child;

  const _InputSection({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.child,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Icon(icon, size: 18, color: theme.colorScheme.primary),
            const SizedBox(width: 8),
            Text(
              title,
              style: theme.textTheme.titleSmall?.copyWith(
                fontWeight: FontWeight.w600,
              ),
            ),
          ],
        ),
        const SizedBox(height: 4),
        Padding(
          padding: const EdgeInsets.only(left: 26),
          child: Text(
            subtitle,
            style: theme.textTheme.bodySmall?.copyWith(
              color: theme.colorScheme.onSurface.withValues(alpha: 0.5),
            ),
          ),
        ),
        const SizedBox(height: 10),
        child,
      ],
    );
  }
}
