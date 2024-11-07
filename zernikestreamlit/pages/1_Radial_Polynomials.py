import streamlit as st
from mocapy.zernike import Radial
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sympy as sp

st.title("Radial Polynomials")
st.write(
    r"While actually being a function of 1 variable, $\rho$, we display the polynomials as 2D functions so "
    "it's easier to relate to Zernike polynomials later. To do so, the 1D polynomial is just 'expanded' as a "
    "rotationally symmetric function."
)

# Sidebar
st.sidebar.header("Input Options")
st.sidebar.markdown("## Table of Contents")
st.sidebar.markdown("""
- [Quick plot inspection](#radial-inspecter)
- [Equations](#equations)
- [Expressions for first polynomials](#expression-for-the-first-few-radials)
- [Normalisation and orthogonality](#normalisation-and-orthogonality)
- [Evaluating](#evaluating)
""")

# Intro plot
@st.cache_resource
def intro_3d_plot(n=7, m=1):
    fig = Radial(n, m).plot_3d_plotly()
    fig.update_layout(title=f"Radial(n={n}, m={m})")
    return fig

st.plotly_chart(intro_3d_plot(), use_container_width=True)

# Definition Section
@st.cache_resource
def definition_content():
    st.header("Definition")
    st.write(r"Radial function is denoted $r_{n}^m$, for $n \ge m \ge 0$ and $n, m \in \mathbb{N}$:")
    st.latex(r"""
    r_n^m(\rho) =
    \begin{cases}
        \sum_{i=0}^{(n-m)/2} \frac{(-1)^i (n-i)!}{i!(\frac{n+m}{2}-i)!(\frac{n-m}{2}-i)!}\rho^{n-2i} & \text{for $n-m$ even} \\
        0 & \text{for $n-m$ odd} \\
    \end{cases}
    """)

    st.write("Alternative definitions are based on:")
    st.write("- Gamma function:")
    st.latex(r"r_n^m(\rho) =\frac{\Gamma(n+1)F_{12}(-\frac{m+n}{2}, \frac{m-n}{2}; -n;\rho^{-2})}{\Gamma(\frac{2+n-m}{2}\Gamma(\frac{2+n+m}{2}))}")

    st.write("- Jacobi polynomials:")
    st.latex(r"r_n^m(\rho) = (-1)^{(n-m)/2} \rho^m P_{(n-m)/2}^{(m,0)}(1-2\rho^2)")

    st.write("To create a radial polynomial for two integers `n` and `m` that satisfy:")
    st.markdown(r"""
    - $n, m \ge 0$  
    - $n \ge m$  
    - $(n-m)\%2 = 0$  
    """)

    st.code("""
    >>> from mocapy.zernike import Radial
    >>> n, m = 2, 2
    >>> r = Radial(n, m)
    >>> r
    <Radial(n=2, m=2, ortho_norm=False) : rho**2>
    """, language="python")

definition_content()

# Evaluation Section
st.header("Evaluating")
@st.cache_data
def static_evaluation_content():
    st.write(r"""
    Several options are available to evaluate a polynomial, either as a 1D function of $\rho$, or as a 2D function of $x, y$.
    - using `r(0.5)`, relies on the `__call__` method
    """)
    st.code(">>> r(0.5)\n0.25")

    st.write("- using `r.cart(x, y)` to evaluate in the 2D plane with a numpy grid:")
    st.code("""
    >>> rhos = np.linspace(0, 1, 100)
    >>> thetas = np.linspace(0, 2 * np.pi, 100)
    >>> r_grid, theta_grid = np.meshgrid(rhos, thetas)
    >>> x, y = r_grid * np.cos(theta_grid), r_grid * np.sin(theta_grid)
    >>> r.cart(x, y)
    """, language="python")

static_evaluation_content()

# Radial Inspector Section
st.header("Radial Inspector")
st.write("Use the controls to visualize the polynomial based on indices `n` and `m`.")
def evaluate_radial_polynomial(n, m, rho):
    try:
        return Radial(n, m)(rho)
    except Exception as e:
        return str(e)

col1, col2, col3 = st.columns(3)
with col1:
    st.number_input("`n`", min_value=0, max_value=10, value=0, key='n_input')
with col2:
    st.number_input("`m`", min_value=0, max_value=10, value=0, key='m_input')
with col3:
    ortho_norm = st.checkbox("`ortho_norm`")

r = Radial(st.session_state.n_input, st.session_state.m_input, ortho_norm)

col1, col2 = st.columns(2)
with col1:
    try:
        st.code(f">>> r = Radial(n={st.session_state.n_input}, m={st.session_state.m_input}, ortho_norm={ortho_norm})")
        st.latex(rf"r_{{{st.session_state.n_input}}}^{{{st.session_state.m_input}}}(\rho) = {sp.latex(r._expr)}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

with col2:
    try:
        fig = r.plot_3d_plotly()
        fig.update_layout(title="")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"An error occurred while plotting: {str(e)}")

# Normalization Section
@st.cache_data
def display_normalization_content():
    st.header("Normalization and Orthogonality")
    st.latex(r"r_n^{m} \cdot r_{n'}^{m} = \int_0^1 r_n^m(\rho)r_{n'}^m(\rho) \rho d\rho = \frac{\delta_{n,n'}}{2n+2}")

    st.write("To calculate the dot product:")
    st.code("""
    >>> r_22 = Radial(n=2, m=2)
    >>> r_42 = Radial(n=4, m=2)
    >>> print(r_22.dot(r_42))  # Expect 0
    >>> print(r_22.dot(r_22))  # Expect 1/6
    """, language="python")

display_normalization_content()

# Radial Helpers Section
st.header("Radial Class Helpers")
st.subheader("1D Plots")
st.markdown("Plotting the 1D for the N first polynomials.")
@st.cache_data
def cached_plot_1D(N=10):
    fig = Radial.plot_1D(N=N)
    return fig

st.pyplot(cached_plot_1D())

st.subheader("2D Plots")
@st.cache_data
def cached_plot_2D(N=30):
    fig = Radial.plot_2D(N=N)
    return fig

st.pyplot(cached_plot_2D())

st.subheader("3D Plot")
@st.cache_resource
def cached_plot_3D():
    fig = Radial.plot_3D()
    return fig

st.pyplot(cached_plot_3D())

st.dataframe(Radial.summup())
