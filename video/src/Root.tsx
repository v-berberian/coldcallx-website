import {Composition} from 'remotion';
import {Promo, promoSchema} from './Promo';

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="Promo"
      component={Promo}
      durationInFrames={150}
      fps={30}
      width={1920}
      height={1080}
      schema={promoSchema}
      defaultProps={{
        title: 'ColdCallX',
        subtitle: 'The auto dialer built for closers',
      }}
    />
  );
};
