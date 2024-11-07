import streamlit as st
from mocapy.zernike import Zernike, WaveFront


st.header("Definition")
st.markdown(r"A WFE is just a linear combination of zernike polynomials")       
st.latex(r'WFE(\rho, \theta) = \sum_i a_iZ_i(\rho, \theta)')
st.write(r"""In other words, in the L2 space on the unit disk, the Zernike polynomials are the canonical vectors $(e_i)$, and wavefronts are the vectors of that space.
Using matrix notations : 
""")
st.latex(r"""\left< Z \right| = |Z_0, ..., Z_J|""")
st.latex(r"""\left| a \right> = |a_0, ..., a_J|""")
st.latex(r"""WFE = \left< Z | a \right>""")


st.header('Zernike transform')
st.write('We now have a framework that provides an infinit set of orthogonal polynomials, so just like the Fourier transform but for the unit disk, we can define the Zernike trasnsform:')
st.latex(r"G(\rho, \phi) = \sum_{m,n}a_{m,n}Z_n^m(\rho, \phi) + b_{m,n}Z_n^{-m}(\rho, \phi)")
st.write("where the a and b coeffients are computed using the inner product from before:")
st.latex(r"<F;G > = \int F(\rho, \phi)G(\rho, \phi)\rho d\rho d\phi")
st.write("then")
st.latex(r"a_{m,n}= \frac{2n+2}{\epsilon_m \pi}<G;Z_n^m>")
st.latex(r"b_{m,n}= \frac{2n+2}{\epsilon_m \pi}<G;Z_n^{-m}>")

st.header('Rotation')
st.write(r'By definition, Zernike polynomials and wavefront are defined using coordinates relative to x-y axis. What happens if the surface is rotated relative to those coordinates, or in other words, what happens if we want to express the wrave in a new, rotated coordinate system ? Well it turns out we can just compute new zernike coefficients:')
st.write(r"We write the definition using a new angle theta + alpha, and identify the terms using new coefficients b to compare to. In the original space, the wavefront coefficients are noted $a_n^{\pm m}$, and in the new space $b_n^{\pm m}$, we just need to find an expression of the b coefficients from the a coefficients:")
st.latex(r"W(\rho, \theta+\alpha) = \sum_{n=0}^{\infty} \sum_{m=0}^n \left[ a_n^{m}Z_n^m(\rho, \theta+\alpha) +  a_n^{-m}Z_n^{-m}(\rho, \theta+\alpha)\right]")
st.latex(r"= \sum_{n=0}^{\infty} \sum_{m=0}^n  \left[ a_n^{m}R_n^m(\rho) \cos(m(\theta+\alpha)) +  a_n^{-m}R_n^{-m}(\rho) \sin(m(\theta+\alpha))\right]")
st.latex(r"= \sum_{n=0}^{\infty} \sum_{m=0}^n  \left[ b_n^{m}R_n^m(\rho) \cos(m\theta) +  b_n^{-m}R_n^{-m}(\rho) \sin(m\theta)\right]")
st.write("where we now want to express the b coefficients.")
st.write("With:")
st.latex(r"\sum_{n=0}^{\infty} \sum_{m=0}^n  \left[ a_n^{m}R_n^m(\rho) \cos(m(\theta+\alpha)) +  a_n^{-m}R_n^{-m}(\rho) \sin(m(\theta+\alpha))\right]")
st.latex(r"""= \sum_{n=0}^{\infty} \sum_{m=0}^n  \left[ a_n^{m}R_n^m(\rho) \left(\cos(m\theta)\cos(m\alpha) - \sin(m\theta)\sin(m\alpha) \right) + \\
a_n^{-m}R_n^{-m}(\rho) \left(\cos(m\theta)\sin(m\alpha) + \sin(m\theta)\cos(m\alpha) \right) \right]""")

st.latex(r"= \sum_{n=0}^{\infty} \sum_{m=0}^n  \left[a_n^{m}\cos(m\alpha) + a_n^{-m}\sin(m\alpha)  \right] R_n^m(\rho)\cos(m\theta) + \left[-a_n^{m}\sin(m\alpha) + a_n^{-m}\cos(m\alpha)  \right] R_n^{-m}(\rho)\sin(m\theta)")
st.write("hence")
st.latex(r"b_n^{m} = \left[a_n^{m}\cos(m\alpha) + a_n^{-m}\sin(m\alpha)  \right]")
st.latex(r"b_n^{-m} = \left[-a_n^{m}\sin(m\alpha) + a_n^{-m}\cos(m\alpha)  \right]")
st.write('It is important to note that if the input wavefront has say only 1 coefficient $a_n^m$ with m>0, in the rotated system the wavefront will have 2 coefficients')

st.write(r"""This analytical result can be verified numerically using an example.\n
First, we define a wavefront using `wfe = WaveFront({(5, 3): 2, (3, 1): -0.5})`, so it has 2 coefficients $a_5^3=2$ and $a_3^1-0.5$
for zernikes $(n=5,m=3)$ and $(n=3,m=1)$ respectively, the other coefficients being 0.
We want to evaluate the zernike deomposition using a new coordinate system, rotated from the
original one of an anlge of `new_angle = theta + np.pi / 5`. Then, we can compute the new coefficients using:
""")
st.code(r"""
def b_n_m(a_n_m, a_n_mm, alpha, m):
    return a_n_m * np.cos(m * alpha) + a_n_mm * np.sin(m * alpha)

def b_n_mm(a_n_m, a_n_mm, alpha, m): # mm means "minus m"
    return -a_n_m * np.sin(m * alpha) + a_n_mm * np.cos(m * alpha)     
""")
st.write('Based on those functions, we know how to define a new wavefront in that new coordinate system')
st.code(r"""
>>> # for n=5
>>> print(f"b_5^3 = {b_n_m(2, 0, np.pi/5, 3)}")
        
>>> # for n=3
>>> print(f"b_3^1 = {b_n_m(-0.5, 0, np.pi/5, 1)}")

>>> # for n=5
>>> print(f"b_5^-3 = {b_n_mm(2, 0, np.pi/5, 3)}")

>>> # for n=3
>>> print(f"b_3^-1 = {b_n_mm(-0.5, 0, np.pi/5, 1)}")
        
""")
st.write('So we know that this new wavefront should have 4 coefficients/zernike polynomials.')
st.write('On the other hand, we can check those computation and that approach overall by decomposing the rotated wavefront using the zernike transform: thanks to the propeties of the zernike polynomials, we know that any surface on the unit disk can be uniquely decomposed as a linear combination of zernike polynomials (just like a signal is decomposed unsing its Discrete Fourier Transform (DFT). This means that we can provide the 2 surface, and extract the value for each coefficient.')

st.code(r"""
>>> rho = np.linspace(0, 1, 101)
>>> theta = np.linspace(0, 2 * np.pi, 101)
>>> rho, theta = np.meshgrid(rho, theta)
>>> x = rho * np.cos(theta)
>>> y = rho * np.sin(theta)
>>> new_angle = theta + np.pi / 5
>>> wfe = WaveFront({(5, 3): 2, (3, 1): -0.5})
>>> # evaluate the rotated 2d surface 
>>> zs = wfe(rho, new_angle)
>>> # extract the wavefront decomposition from the rotated, sampled surface
>>> wfe_from_fitted = WaveFront.from_sampled_wavefront(x, y, zs)
>>> print(wfe_from_fitted.coefs)
""")    
st.write('This shows that the analytical computation of the new coefficients and the numerical decomposition give the same results, which is quite satisfying and reassuring!')


col1, col2, col3 = st.columns([0.15, 0.45, 0.45])

with col1:
    n1 = st.number_input("`n_1`", min_value=0, max_value=10, value=0, key='n_input1')
    m1 = st.number_input("`m_1`", min_value=0, max_value=10, value=0, key='m_input1')
    n2 = st.number_input("`n_2`", min_value=0, max_value=10, value=0, key='n_input2')
    m2 = st.number_input("`m_2`", min_value=0, max_value=10, value=0, key='m_input2')

z1 = Zernike(n1, m1)
z2 = Zernike(n2, m2)

with col2:
    fig = z1.plot_3d_plotly(cb=False)
    st.plotly_chart(fig, use_container_width=True)

with col3:
    fig = z2.plot_3d_plotly(cb=False)
    st.plotly_chart(fig, use_container_width=True)

wfe = z1 + z2
fig = wfe.plot_3d_plotly()
st.plotly_chart(fig, use_container_width=True)

st.header("Other Normalization Convention")
st.write("Another convention sometimes used for normalizing the polynomials:")
st.latex(r"""
\int_0^{2\pi} \int_0^1 Z'_j(\rho, \theta)Z'_{j'}(\rho, \theta)\rho d\rho d\theta = \pi \delta_{jj'}
""")

st.header("Translation")
st.write("For a translated coordinate system, the polynomials' coefficients adjust as:")
st.latex(r"""
W(x-\Delta x, y-\Delta y) = \sum_{n,m} a_{n,m} \sum_{i=0}^{\infty} \frac{(-1)^s}{s!} \left( \Delta x \frac{\partial}{\partial x} + \Delta y \frac{\partial}{\partial y} \right)^{s-th} Z_{n,m}(\rho, \theta)
""")
