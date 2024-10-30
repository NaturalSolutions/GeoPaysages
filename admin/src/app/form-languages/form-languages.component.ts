import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { NgbModal, NgbModalRef, NgbTabChangeEvent } from '@ng-bootstrap/ng-bootstrap';
import { FormGroup } from '@angular/forms';
import { FormService } from '../services/form.service';
import { Conf } from './../config';
import * as _ from 'lodash';
import { ToastrService } from 'ngx-toastr';
import { AuthService } from '../services/auth.service';
import { NgxSpinnerService } from 'ngx-spinner';
import { Language, LanguagePatchType} from '../types';
import * as io from 'jsts/org/locationtech/jts/io';
import { TranslateService } from '@ngx-translate/core';
import { combineLatest, Observable } from 'rxjs';
import { TranslationService } from '../services/translation.service';
import { LanguageService } from '../services/language.service';

@Component({
  selector: 'app-form-languages',
  templateUrl: './form-languages.component.html',
  styleUrls: ['./form-languages.component.scss'],
})
export class FormLanguagesComponent implements OnInit {
//   @ViewChild('thumbnailInput') thumbnailInput;
//   @ViewChild('logoInput') logoInput;

  selectedThumb: File;
  selectedLogo: File;
  selectedFile: File[];
  modalRef: NgbModalRef;
  selectedSubthemes = [];
  thumbs = [];
  noticeName: any;
  new_notice: any;
  languageForm: FormGroup;
  languageJson;
  themes: any;
  subthemes: any;
  loadForm = false;
  mySubscription;
  id_language = null;
  photoBaseUrl = Conf.img_srv;
  previewImage: string | ArrayBuffer;
  alert: { type: string; message: string };
  language: Language;
  isEditing = false;
  edit_btn_text = 'BUTTONS.EDIT';
  submit_btn_text = 'BUTTONS.ADD';
  initThumbs: any[] = [];
  deleted_thumbs = [];
  new_thumbs = [];
  toast_msg: string;
  communes: undefined;
  currentUser: any;
  removed_notice: any = null;
  availableLang: Language[]
  currentTabLangId: string;
  errorMessage: string = 'test';
  isInvalidForm: boolean = false;
  defaultLang:Language;

  constructor(
    public formService: FormService,
    protected router: Router,
    private route: ActivatedRoute,
    private toastr: ToastrService,
    private modalService: NgbModal,
    private authService: AuthService,
    private spinner: NgxSpinnerService,
    private translate: TranslateService,
    private languageService: LanguageService
  ) {}

  ngOnInit() {
    // this.availableLang = this.languageService.getLanguagesDB()
    // this.defaultLang = this.languageService.getDefaultLanguageDB();
    // this.currentTabLangId =  this.availableLang[0].id;
    this.currentUser = this.authService.currentUser;
    this.id_language = this.route.snapshot.params['id'];
    this.languageForm = this.formService.initFormlanguage();
    if (this.id_language) {
      this.getlanguage(this.id_language);
      this.submit_btn_text = 'BUTTONS.SUBMIT';
    } else {
      this.isEditing = true;
      this.loadForm = true;
    }
  }

  async submitlanguage(languageForm) {

    languageForm.updateValueAndValidity();
    console.log('SUBMIT languageForm', languageForm);
    this.alert = null;
    console.log("languageForm.valid", languageForm.valid);
    console.log("this.languageForm.valid", this.languageForm.valid);
    const isValidForm = this.formService.checkAllControlStatuses(languageForm);
    if (!isValidForm) {
      this.isInvalidForm = true;
      this.errorMessage =this.generateErrorMessage();
      console.log("this.errorMessage", this.errorMessage);
      return;
    }
    this.isEditing = false;
    this.spinner.show();
    try {
      if (!this.id_language) {
        const res = await this.postlanguage();
        console.log('res', res);
        this.router.navigate(['languages', 'details', res.id]);
        return;
      } else {
        this.patchlanguage();
      }
    } catch (err) {
      if (err.status === 403) {
        this.translate.get('ERRORS.SESSION_EXPIRED').subscribe((message: string) => {
          this.router.navigate(['']);
          this.toastr.error(message, '', {
            positionClass: 'toast-bottom-right',
          });
        });
      } else {
        this.translate.get('ERRORS.SERVER_ERROR').subscribe((message: string) => {
          this.toastr.error(message, '', {
            positionClass: 'toast-bottom-right',
          });
        });
      }
    }
    this.edit_btn_text = 'BUTTONS.EDIT';
    this.spinner.hide();
  }

  setAlert(message: string) {
    this.translate.get('ALERTS.ITEM_EXISTS').subscribe((translatedMessage: string) => {
      this.alert = {
        type: 'danger',
        message: `${translatedMessage.replace('{{ item }}', message)}`,
      };
    });
  }
  getlanguage(id_language) {
    this.languageService.getById(id_language).subscribe(
      (language) => {
        this.language = language;
      },
      (err) => {
        console.log('err', err);
        this.translate.get('ERRORS.SERVER_ERROR').subscribe((message: string) => {
          this.toastr.error(message, '', {
            positionClass: 'toast-bottom-right',
          });
        })
      },
      () => {
        this.patchForm();
        this.loadForm = true;
        this.languageForm.disable();
      }
    );
  }

  postlanguage(): Promise<Language> {
    return new Promise((resolve, reject) => {
      const formValue = this.languageForm.value;
      const post: Language = this.createPostObject(formValue);
    
      this.languageService.post(post).subscribe(
        (res) => {
          this.translate.get("INFO_MESSAGE.SUCCESS_ADDED_LANG").subscribe((message: string) => {
            this.toastr.success(message, '', {
              positionClass: 'toast-bottom-right',
            })
          resolve(res);
          });
        },
        (err) => {
          reject(err);
        }
      );
    });
  }

  patchlanguage(): Promise<void> {
    return new Promise((resolve, reject) => {
    const { id, ...patch } = this.languageForm.value;
    const typedPatch: LanguagePatchType = patch;
      console.log("typedPatch", typedPatch)
      this.languageService.patch(id, typedPatch).subscribe(
        (res) => {
          this.translate.get("INFO_MESSAGE.SUCCESS_UPDATED_LANG").subscribe((message: string) => {
            this.toastr.success(message, '', {
              positionClass: 'toast-bottom-right',
            })
          });
          resolve();
        },
        (err) => {
          reject(err);
        }
      );
    });
  }


  editForm() {
    this.isInvalidForm = false;
    this.isEditing = !this.isEditing;
    if (!this.isEditing) {
      this.edit_btn_text = 'BUTTONS.EDIT';
      this.patchForm();
      this.alert = null;
      this.languageForm.disable();
    } else {
      this.edit_btn_text = 'BUTTONS.CANCEL';
      this.languageForm.enable();
    }
  }

  openDeleteModal(content) {
    this.modalRef = this.modalService.open(content, {
      windowClass: 'delete-modal',
      centered: true,
    });
  }

  cancelDelete() {
    this.modalRef.close();
  }

  onCancel() {
    this.languageForm.reset();
    this.router.navigate(['languages']);
  }

  patchForm() {
    this.languageForm.patchValue(this.language);
    this.languageForm.patchValue({
      label: this.language.label,
      id: this.language.id,
      is_default: this.language.is_default,
      is_published: this.language.is_published,
    })
}


  ngOnDestroy() {
    this.languageService.loadLanguagesSorted()
    this.spinner.hide();
    if (this.mySubscription) {
      this.mySubscription.unsubscribe();
    }
  }

  // Méthode appelée lors du changement d'onglet
  changeTab(event: NgbTabChangeEvent): void {
    this.currentTabLangId = event.activeId;
  }
  
  getTranslatedMessages(keys: string[]): Observable<string[]> {
    return combineLatest(keys.map(key => this.translate.get(key)));
  }
  private generateErrorMessage(): string {
    return "Veuillez vérifier tous les champs obligatoires dans chaque onglet"
    // return this.formService.generateErrorMessage(this.languageForm,[], formLabels.language);
 }

 createPostObject(formValue): Language {
  // Récupérez les propriétés de base
  const post: Language = {
    label: formValue.label,
    id: formValue.id,
    is_default: formValue.is_default,
    is_published: formValue.is_published,
  };
  return post;
}

}
