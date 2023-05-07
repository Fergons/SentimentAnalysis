<!-- Created by Frantisek Sabol -->
<script lang="ts">
    import {onDestroy, onMount} from 'svelte';
    import {mdiWeatherNight, mdiWeatherSunny} from '@mdi/js';
    import TinyGesture from 'tinygesture';
    import {page} from '$app/stores';
    import TopAppBar, {Row, Section, Title} from '@smui/top-app-bar';
    import Drawer, {AppContent, Content, Header, Scrim} from '@smui/drawer';
    import IconButton from '@smui/icon-button';
    import Button, {Label} from '@smui/button';
    import List, {Item, Separator, Text} from '@smui/list';
    import Tooltip, {Wrapper} from '@smui/tooltip';
    import {Icon, Svg} from '@smui/common';
    import userStore from '../lib/stores/user';
    import type {User} from "../lib/client";
    import {applyAction, enhance} from "$app/forms";
    import type {LayoutServerData} from "../../.svelte-kit/types/src/routes/$types";
    import {invalidateAll} from "$app/navigation";
    import {browser} from "$app/environment";

    export let data: LayoutServerData;
    const defaultUser = browser ?
        window.localStorage.getItem('user') ? JSON.parse(window.localStorage.getItem('user')) : null : null;

    let topAppBar: TopAppBar;
    let currentPageTitle = '';
    let drawer: Drawer;
    let mainContent: HTMLElement;
    let miniWindow = false;
    let drawerOpen = false;
    let drawerGesture: TinyGesture;
    let mainContentGesture: TinyGesture;
    let innerWidth: number = 0;
    let innerHeight: number = 0;

    let lightTheme = false;
    let activeSection: DrawerSection | undefined = undefined;
    let lastPagePath: string | undefined = undefined;

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
        comingSoon?: boolean;
        mdcIcon?: string;
        indent?: number;
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
            comingSoon: false,
            indent: 0
        },
        {
            name: 'Movies',
            comingSoon: true,
        },
        {
            name: 'Books',
            comingSoon: true,
        },
        {
            name: 'Laptops',
            comingSoon: true,
        },
        {
            name: '+ Create Your Own',
            mdcIcon: 'plus',
            comingSoon: true,
        }
    ];

    $: activeSection = sections.find(
        (section) => 'route' in section && routesEqual(section.route ?? '', $page.url.pathname)
    ) as DrawerSection | undefined;
    let previousPagePath: string | undefined = undefined;

    $:  {
        currentPageTitle = activeSection ? activeSection.name : $page.data ? $page.data.name : '';
        $page.data.subtitle ? currentPageTitle = currentPageTitle + " | " + $page.data.subtitle : currentPageTitle = currentPageTitle;
        currentPageTitle = currentPageTitle ? currentPageTitle : "";
    }

    $: if (mainContent && previousPagePath !== $page.url.pathname) {
        drawerOpen = false;
        const hashEl =
            window.location.hash && document.querySelector<HTMLElement>(window.location.hash);
        mainContent.scrollTop = (hashEl && hashEl.offsetTop) || 0;
        lastPagePath = previousPagePath;
        previousPagePath = $page.url.pathname;
    }

    $: if (innerWidth > 0 && innerHeight > 0) {
        setMiniWindow();
    }

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
            miniWindow = window.innerWidth < 1200;
        }
    }
</script>

<svelte:window bind:innerWidth bind:innerHeight/>

<div class="drawer-container">
    <Drawer
            bind:this={drawer}
            variant={miniWindow ? 'modal' : undefined}
            bind:open={drawerOpen}
            class="app-drawer mdc-theme--secondary-bg {miniWindow
			? 'app-drawer-adjust'
			: 'hide-initial-small'}"
    >
        <Header style="display:flex; justify-content: space-between; height: 66px;  flex-direction: column; padding-bottom: 0">
            <div style="display:flex; flex-direction: column; height: 100%; justify-content: center">
                <Title style="padding-left:0"><a href="/" style="color:inherit; text-decoration: inherit">SNTMNT</a>
                </Title>
            </div>
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
                            <Text>{section.name}</Text>
                            {#if section.comingSoon}
                               <span class="mdc-typography--caption"
                                     style="color: #5d5d78;
                                     font-size: 12px;
                                     margin-left: 8px;"
                               >coming soon!</span>
                            {/if}

                        </Item>
                    {/if}
                {/each}
            </List>
        </Content>
    </Drawer>
    {#if miniWindow}
        <Scrim/>
    {/if}
    <AppContent class="app-content">
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
                            style={miniWindow ? 'padding-left: 0;' : ''}
                    >
                        {miniWindow ? '' : currentPageTitle}
                    </Title>
                </Section>

                <Section align="end" toolbar style="color: #000;">

                    {#if $userStore}
                        <Button tag="a" href="/users/me">{$userStore.email}</Button>
                        <form action="/signout" method="POST" use:enhance={() => {
                            console.log("signout");
                            return async ({result}) => {
                                console.log("result signout");
                                $userStore = null;
                                await invalidateAll();
                                await applyAction(result);
                            }
                        }}>
                            <Button>Sign out</Button>
                        </form>
                    {:else}
                        <Button href="/signin">Signin</Button>
                        <Button href="/signup">Signup</Button>
                    {/if}
                    <Wrapper>
                        <IconButton toggle pressed={lightTheme} on:SMUIIconButtonToggle:change={switchTheme}>
                            <Icon component={Svg} viewBox="0 0 24 24" on>
                                <path fill="currentColor" d={mdiWeatherNight}></path>
                            </Icon>
                            <Icon component={Svg} viewBox="0 0 24 24">
                                <path fill="currentColor" d={mdiWeatherSunny}></path>
                            </Icon>
                        </IconButton>
                        <Tooltip>{lightTheme ? 'Lights off' : 'Lights on'}</Tooltip>
                    </Wrapper>
                </Section>
            </Row>
        </TopAppBar>
        <main class="app-main-content" bind:this={mainContent}>
            <slot/>
        </main>
    </AppContent>
</div>

<style>
</style>
