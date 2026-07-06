import 'package:flutter/material.dart';

class BudgetSelector extends StatelessWidget {
  final String selected;
  final ValueChanged<String> onChanged;

  const BudgetSelector({
    super.key,
    required this.selected,
    required this.onChanged,
  });

  static const _options = ['\$', '\$\$', '\$\$\$', '\$\$\$\$'];
  static const _labels = ['Budget', 'Moderate', 'Pricey', 'Splurge'];

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Row(
      children: List.generate(_options.length, (i) {
        final isSelected = selected == _options[i];
        return Expanded(
          child: Padding(
            padding: EdgeInsets.only(
              left: i == 0 ? 0 : 6,
              right: i == _options.length - 1 ? 0 : 6,
            ),
            child: GestureDetector(
              onTap: () => onChanged(_options[i]),
              child: AnimatedContainer(
                duration: const Duration(milliseconds: 200),
                padding: const EdgeInsets.symmetric(vertical: 12),
                decoration: BoxDecoration(
                  color: isSelected
                      ? theme.colorScheme.primary
                      : theme.colorScheme.surfaceContainerHighest,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(
                    color: isSelected
                        ? theme.colorScheme.primary
                        : Colors.transparent,
                  ),
                ),
                child: Column(
                  children: [
                    Text(
                      _options[i],
                      style: theme.textTheme.titleMedium?.copyWith(
                        color: isSelected
                            ? theme.colorScheme.onPrimary
                            : theme.colorScheme.onSurface,
                        fontWeight: isSelected
                            ? FontWeight.bold
                            : FontWeight.normal,
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      _labels[i],
                      style: theme.textTheme.labelSmall?.copyWith(
                        color: isSelected
                            ? theme.colorScheme.onPrimary.withValues(alpha: 0.8)
                            : theme.colorScheme.onSurface.withValues(
                                alpha: 0.6,
                              ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        );
      }),
    );
  }
}
