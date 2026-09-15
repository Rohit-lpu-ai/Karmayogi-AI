// jsdom gaps needed by Radix primitives and sonner. Test-only; never shipped.
if (!window.matchMedia) {
  window.matchMedia = (query: string) =>
    ({
      matches: false,
      media: query,
      onchange: null,
      addListener: () => undefined,
      removeListener: () => undefined,
      addEventListener: () => undefined,
      removeEventListener: () => undefined,
      dispatchEvent: () => false,
    }) as MediaQueryList;
}

if (!("ResizeObserver" in window)) {
  class ResizeObserverStub {
    observe() {}
    unobserve() {}
    disconnect() {}
  }
  (window as unknown as { ResizeObserver: typeof ResizeObserverStub }).ResizeObserver = ResizeObserverStub;
}

const elementProto = Element.prototype as unknown as Record<string, unknown>;
elementProto.hasPointerCapture ??= () => false;
elementProto.setPointerCapture ??= () => undefined;
elementProto.releasePointerCapture ??= () => undefined;
elementProto.scrollIntoView ??= () => undefined;
