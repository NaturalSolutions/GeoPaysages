export type ObservatoryType = {
  id: number;
  ref: string;
  color: string;
  thumbnail: string;
  logo: string;
  comparator: string;
  geom: any;
  translations:{
    lang_id: string;
    is_published: boolean;
    title: string;
  }[]
};

export type ObservatoryPostType = Pick<
  ObservatoryType,
  'ref' | 'color' | 'geom'
> & {
  is_published: boolean; // Il semble que is_published doive être pris à partir des traductions
  title: string; // Title doit également provenir de translations, mais le type a besoin de clarification
};
export type ObservatoryPatchType = Partial<ObservatoryPostType>;

export type ObservatoryPatchImageType = {
  filename: string;
};
