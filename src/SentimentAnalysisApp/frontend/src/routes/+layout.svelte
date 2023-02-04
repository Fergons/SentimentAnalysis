<script lang="ts">
    import {onDestroy, onMount} from 'svelte';
    import {mdiFileDocument, mdiWeatherSunny, mdiWeatherNight} from '@mdi/js';
    import {siDiscord, siTwitter, siGithub} from 'simple-icons/icons';
    import TinyGesture from 'tinygesture';
    import {assets} from '$app/paths';
    import {page} from '$app/stores';
    import TopAppBar, {Row, Section, Title} from '@smui/top-app-bar';
    import Drawer, {Content, Scrim, AppContent, Header, Subtitle} from '@smui/drawer';
    import IconButton from '@smui/icon-button';
    import List, {Item, Text, Separator, PrimaryText, Label} from '@smui/list';
    import Tooltip, {Wrapper} from '@smui/tooltip';
    import {Icon, Svg} from '@smui/common';
    import {mdiGithub, mdiWeb, mdiChevronLeft} from '@mdi/js';

    let topAppBar: TopAppBar;
    let currentPageTitle = '...';
    let drawer: Drawer;
    let mainContent: HTMLElement;
    let miniWindow = false;
    let drawerOpen = false;
    let drawerGesture: TinyGesture;
    let mainContentGesture: TinyGesture;

    let lightTheme: boolean;
    let activeSection: DrawerSection | undefined;
    let lastPagePath: string | undefined;

    function switchTheme() {
        lightTheme = !lightTheme;
        let themeLink = document.head.querySelector<HTMLLinkElement>('#theme');
        if (!themeLink) {
            themeLink = document.createElement('link');
            themeLink.rel = 'stylesheet';
            themeLink.id = 'theme';
        }
        themeLink.href = `/smui${lightTheme ? '' : '-dark'}.css`;
        document.head
            .querySelector<HTMLLinkElement>('link[href$="/smui-dark.css"]')
            ?.insertAdjacentElement('afterend', themeLink);
    }

    type DrawerSection = {
        component?: InstanceType<typeof Item>;
        name: string;
        route?: string;
        shortcut?: string;
        title: string;
        indent: number;
    };

    const sections: (
        | DrawerSection
        | {
        name: string;
        separator: true;
    }
        )[] = [
        {
            name: 'Games',
            route: '/games',
            title: 'Games',
            indent: 0
        },
        {
            name: 'Home',
            title: 'Home',
            route: '/',
            indent: 0
        },
        {
            name: 'About',
            title: 'About',
            route: '/about',
            indent: 0
        }
    ];

    $: activeSection = sections.find(
        (section) => 'route' in section && routesEqual(section.route ?? '', $page.url.pathname)
    ) as DrawerSection | undefined;
    let previousPagePath: string | undefined = undefined;
    $: if (mainContent && previousPagePath !== $page.url.pathname) {
        drawerOpen = false;
        const hashEl =
            window.location.hash && document.querySelector<HTMLElement>(window.location.hash);
        const top = (hashEl && hashEl.offsetTop) || 0;
        mainContent.scrollTop = top;
        lastPagePath = previousPagePath;
        previousPagePath = $page.url.pathname;
        currentPageTitle = $page.data.title ?? activeSection?.title ?? '...';
        $page.data.title ?
            currentPageTitle = currentPageTitle + " | " + $page.data.subtitle
            :
            currentPageTitle = currentPageTitle;

    }

    onMount(setMiniWindow);
    onMount(() => {
        if (mainContent) {
            mainContentGesture = new TinyGesture(mainContent, {
                mouseSupport: false
            });
            let touchStartX: number = 0;
            mainContentGesture.on('panstart', () => {
                touchStartX = mainContentGesture.touchStartX;
            });
            mainContentGesture.on('swiperight', () => {
                if (touchStartX <= 40) {
                    drawerOpen = true;
                }
            });
        }
        if (drawer) {
            drawerGesture = new TinyGesture(drawer.getElement(), {
                mouseSupport: false
            });
            drawerGesture.on('swipeleft', () => {
                drawerOpen = false;
            });
        }
        lightTheme = window.matchMedia('(prefers-color-scheme: light)').matches;
    });
    onDestroy(() => {
        if (mainContentGesture) {
            mainContentGesture.destroy();
        }
        if (drawerGesture) {
            drawerGesture.destroy();
        }
    });

    function routesEqual(a: string, b: string) {
        return (a.endsWith('/') ? a.slice(0, -1) : a) === (b.endsWith('/') ? b.slice(0, -1) : b);
    }

    function setMiniWindow() {
        if (typeof window !== 'undefined') {
            miniWindow = window.innerWidth < 720;
        }
    }
</script>

<div class="drawer-container">
    <Drawer
            bind:this={drawer}
            variant={miniWindow ? 'modal' : undefined}
            bind:open={drawerOpen}
            class="app-drawer mdc-theme--secondary-bg {miniWindow
			? 'app-drawer-adjust'
			: 'hide-initial-small'}"
    >
        <Header style="padding: 8px 12px; border-bottom: #5d5d78 1px">
            <Title style="align-self: center">SNTMNT</Title>
            <Separator/>
        </Header>
        <Content style="padding-bottom: 22px;">
            <List>
                {#each sections as section (section.name)}
                    {#if 'separator' in section}
                        <Separator/>
                    {:else}
                        <Item
                                bind:this={section.component}
                                nonInteractive={!('route' in section || 'shortcut' in section)}
                                href={'route' in section
								? section.route
								: 'shortcut' in section
								? section.shortcut
								: undefined}
                                activated={section === activeSection}
                                style={section.indent ? 'margin-left: ' + section.indent * 25 + 'px;' : ''}
                        >
                            <Text class="mdc-theme--on-secondary">{section.name}</Text>
                        </Item>
                    {/if}
                {/each}
            </List>
        </Content>
    </Drawer>

    <div class="bar-app-content">
        <TopAppBar variant="static" class="app-top-app-bar">
            <Row>
                <Section>
                    {#if miniWindow}
                        <IconButton class="material-icons" on:click={() => (drawerOpen = !drawerOpen)}
                        >menu
                        </IconButton>
                    {/if}
                    <Title
                            class="--mdc-theme--primary"
                            on:click={() => (activeSection = undefined)}
                            style={miniWindow ? 'padding-left: 0;' : ''}
                    >
                        {miniWindow ? currentPageTitle : currentPageTitle}
                    </Title>
                </Section>
                <Section align="end" toolbar style="color: var(--mdc-on-surface, #000);">
                    <Wrapper>
                        <IconButton toggle pressed={lightTheme} on:SMUIIconButtonToggle:change={switchTheme}>
                            <Icon component={Svg} viewBox="0 0 24 24" on>
                                <path fill="currentColor" d={mdiWeatherNight}/>
                            </Icon>
                            <Icon component={Svg} viewBox="0 0 24 24">
                                <path fill="currentColor" d={mdiWeatherSunny}/>
                            </Icon>
                        </IconButton>
                        <Tooltip>{lightTheme ? 'Lights off' : 'Lights on'}</Tooltip>
                    </Wrapper>
                </Section>
            </Row>
        </TopAppBar>

        {#if miniWindow}
            <Scrim/>
        {/if}
        <AppContent class="app-content">
            <main class="app-main-content" bind:this={mainContent}>
                <slot/>
            </main>
        </AppContent>
    </div>
</div>

<style>
</style>
