import { RumbaGuiPage } from './app.po';

describe('rumba-gui App', () => {
  let page: RumbaGuiPage;

  beforeEach(() => {
    page = new RumbaGuiPage();
  });

  it('should display welcome message', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('Welcome to app!');
  });
});
