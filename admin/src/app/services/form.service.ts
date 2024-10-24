import { Injectable } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { LatlngValidator } from '../shared/latlng-validator';
@Injectable()
export class FormService {
  public disabled = true;

  constructor(private _fb: FormBuilder) {}

  initFormObservatory(): FormGroup {
    const formSite = this._fb.group({
      title: [null, Validators.required],
      ref: [null],
      color: [null],
      is_published: [false],
      geom: [null],
    });
    return formSite;
  }

  initFormSite(availableLang): FormGroup {
    const formSite = this._fb.group({
      ref_site: [null],
      id_observatory: [null, Validators.required],
      lng: [null, { validators: LatlngValidator.lng, updateOn: 'blur' }],
      lat: [null, { validators: LatlngValidator.lat, updateOn: 'blur' }],
      id_theme: [null, Validators.required],
      id_stheme: [null, Validators.required],
      notice: [null],
      main_theme_id: [null],
    });
    // Champs traductibles pour chaque langue
  availableLang.forEach(lang => {
    formSite.addControl(`name_site_${lang.langId}`, this._fb.control(null, Validators.required));
    formSite.addControl(`desc_site_${lang.langId}`, this._fb.control(null));
    formSite.addControl(`testim_site_${lang.langId}`, this._fb.control(null));
    formSite.addControl(`legend_site_${lang.langId}`, this._fb.control(null, Validators.required));
    formSite.addControl(`publish_site_${lang.langId}`, this._fb.control(false));
    formSite.addControl(`code_city_site_${lang.langId}`, this._fb.control(null, Validators.required));
  });
    return formSite;
  }

  initFormPhoto(): FormGroup {
    const formPhoto = this._fb.group({
      id_role: [null],
      display_gal_photo: [false, Validators.required],
      id_licence_photo: [null],
      date_photo: [null],
      // legende_photo: [null],
      filter_date: [null, Validators.required],
      photo_file: [null],
      main_photo: [null],
    });
    return formPhoto;
  }
}
