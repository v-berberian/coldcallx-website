import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {z} from 'zod';

export const promoSchema = z.object({
  title: z.string(),
  subtitle: z.string(),
});

export const Promo: React.FC<z.infer<typeof promoSchema>> = ({
  title,
  subtitle,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const scale = spring({frame, fps, config: {damping: 200}});
  const subtitleOpacity = interpolate(frame, [20, 45], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#0b0f19',
        justifyContent: 'center',
        alignItems: 'center',
        fontFamily: 'system-ui, -apple-system, sans-serif',
        color: 'white',
      }}
    >
      <div style={{fontSize: 120, fontWeight: 800, transform: `scale(${scale})`}}>
        {title}
      </div>
      <div style={{fontSize: 48, opacity: subtitleOpacity, marginTop: 24}}>
        {subtitle}
      </div>
    </AbsoluteFill>
  );
};
