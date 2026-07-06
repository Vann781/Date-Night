import 'dart:math';
import 'package:flutter/material.dart';

class GlowingHeart extends StatefulWidget {
  const GlowingHeart({super.key});

  @override
  State<GlowingHeart> createState() => _GlowingHeartState();
}

class _GlowingHeartState extends State<GlowingHeart>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _pulse;
  late Animation<double> _glow;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1400),
    )..repeat(reverse: true);

    _pulse = Tween<double>(begin: 0.85, end: 1.15).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOutSine),
    );

    _glow = Tween<double>(begin: 0.2, end: 0.8).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOutSine),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        return SizedBox(
          width: 140,
          height: 140,
          child: Stack(
            alignment: Alignment.center,
            children: [
              // Outer glow ring
              Container(
                width: 100 * _pulse.value,
                height: 100 * _pulse.value,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: theme.colorScheme.primary.withValues(alpha: 0.06),
                ),
              ),
              // Mid glow
              Container(
                width: 80 * _pulse.value,
                height: 80 * _pulse.value,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  boxShadow: [
                    BoxShadow(
                      color: theme.colorScheme.primary.withValues(
                        alpha: _glow.value * 0.4,
                      ),
                      blurRadius: 40 * _pulse.value,
                      spreadRadius: 8 * _pulse.value,
                    ),
                  ],
                ),
              ),
              // Inner glow
              Container(
                width: 60 * _pulse.value,
                height: 60 * _pulse.value,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  boxShadow: [
                    BoxShadow(
                      color: theme.colorScheme.primary.withValues(
                        alpha: _glow.value * 0.6,
                      ),
                      blurRadius: 60 * _pulse.value,
                      spreadRadius: 4 * _pulse.value,
                    ),
                  ],
                ),
              ),
              // Heart icon
              Transform.scale(
                scale: _pulse.value,
                child: Icon(
                  Icons.favorite,
                  size: 56,
                  color: theme.colorScheme.primary,
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}

class SparkleParticle extends StatefulWidget {
  final Color color;

  const SparkleParticle({super.key, required this.color});

  @override
  State<SparkleParticle> createState() => _SparkleParticleState();
}

class _SparkleParticleState extends State<SparkleParticle>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _opacity;
  late Animation<double> _drift;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: Duration(milliseconds: 2000 + Random().nextInt(1500)),
    )..repeat(reverse: true);

    _opacity = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(parent: _controller, curve: Curves.easeInOut));

    _drift = Tween<double>(
      begin: 0,
      end: -30 - Random().nextDouble() * 20,
    ).animate(CurvedAnimation(parent: _controller, curve: Curves.easeOut));
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        return Transform.translate(
          offset: Offset(0, _drift.value),
          child: Opacity(
            opacity: _opacity.value,
            child: Container(
              width: 4,
              height: 4,
              decoration: BoxDecoration(
                color: widget.color,
                shape: BoxShape.circle,
              ),
            ),
          ),
        );
      },
    );
  }
}
