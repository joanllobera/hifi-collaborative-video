import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SessionCloseComponent } from './session-close.component';

describe('SessionCloseComponent', () => {
  let component: SessionCloseComponent;
  let fixture: ComponentFixture<SessionCloseComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SessionCloseComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SessionCloseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
