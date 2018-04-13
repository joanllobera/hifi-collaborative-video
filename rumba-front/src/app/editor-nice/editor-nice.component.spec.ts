import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EditorNiceComponent } from './editor-nice.component';

describe('EditorNiceComponent', () => {
  let component: EditorNiceComponent;
  let fixture: ComponentFixture<EditorNiceComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EditorNiceComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EditorNiceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
