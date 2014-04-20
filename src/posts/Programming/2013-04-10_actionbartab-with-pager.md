Title: ActionBar Tab with Pager
Tags: android

There are a number of questions on stackoverflow about this. In Android API, the ActionBar provides you with the capability of navigating Fragments in Tab mode, while Pager enables swiping of Fragments. And sometimes you will want to have both of these to enhance the user experience. This is a tutorial on how to combine both types of navigation in one activity.

In the implementation, the idea is to bind the event listener of ActionBar's TabListener and ViewPager's OnPageChangeListener into one class. So when there is event triggered in one component (tab or pager), you can invoke the respective action on the other. 

    #!java
	public static class TabPagerAdapter extends FragmentPagerAdapter implements ActionBar.TabListener, ViewPager.OnPageChangeListener {

        private SherlockFragmentActivity activity;
        private ViewPager viewPager;
        private List<Fragment> fragments;

        public TabPagerAdapter(SherlockFragmentActivity activity, ViewPager viewPager) {
            super(activity.getSupportFragmentManager());
            this.activity = activity;
            this.viewPager = viewPager;
            this.viewPager.setAdapter(this);
            this.viewPager.setOnPageChangeListener(this);
            this.fragments = new ArrayList<Fragment>();
        }

        public void addTab(ActionBar.Tab tab, Class<? extends Fragment> fragmentClass) throws IllegalAccessException, InstantiationException {
            this.activity.getSupportActionBar().addTab(tab.setTabListener(this));
            fragments.add(fragmentClass.newInstance());
            notifyDataSetChanged();
        }

        @Override
        public void onTabSelected(ActionBar.Tab tab, FragmentTransaction ft) {
            viewPager.setCurrentItem(tab.getPosition());
        }

        @Override
        public void onTabReselected(ActionBar.Tab tab, FragmentTransaction ft) {
            viewPager.setCurrentItem(tab.getPosition());
        }

        @Override
        public void onPageSelected(int i) {
            this.activity.getSupportActionBar().getTabAt(i).select();
        }
        // some interface methods like onTabUnSelected is obmitted for brevity
        ...

        @Override
        public Fragment getItem(int i) {
            return fragments.get(i);
        }

        @Override
        public int getCount() {
            return this.activity.getSupportActionBar().getTabCount();
        }
    }


For example, in `addTab`, besides adding tab with ActionBar.addTab, you need to call notifyDataSetChanged() of the FragmentPagerAdapter as well. The rest is pretty much self-explained. 

In the layout file, declare a Layout with ViewPager component inside: 

    #!xml
	<?xml version="1.0" encoding="utf-8"?>

	<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
              android:orientation="vertical"
              android:layout_width="match_parent"
              android:layout_height="match_parent">
    <android.support.v4.view.ViewPager
        android:id="@+id/pager"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_weight="1"/>
	</LinearLayout> 

In your Activity class, create an instance of TabPagerAdapter and add new Tabs with their respective classes:

    #!java
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        requestWindowFeature(Window.FEATURE_INDETERMINATE_PROGRESS);

        setContentView(R.layout.main);

        final ActionBar ab = getSupportActionBar();

        if (ab.getNavigationMode() != ActionBar.NAVIGATION_MODE_TABS) {
            ab.setDisplayShowTitleEnabled(false);
            ab.setNavigationMode(ActionBar.NAVIGATION_MODE_TABS);
        }

        ViewPager pager = (ViewPager)findViewById(R.id.pager);
        TabPagerAdapter tabPagerAdapter = new TabPagerAdapter(this, pager);

        try {

            tabPagerAdapter.addTab(ab.newTab().setText("Browse"), CategoryListFragment.class);

            tabPagerAdapter.addTab(ab.newTab().setText("Home"), HomeFragment.class);

        } catch (IllegalAccessException e) {
            ...
        } catch (InstantiationException e) {
            ...
        }

    }
